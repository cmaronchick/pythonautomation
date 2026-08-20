"""Scrape Bloodworks Northwest drives for active F3 locations.

The F3 Nation location API is the source of truth for AO names and ZIP codes.
For every active location with a ZIP code, we search Bloodworks using that ZIP.
If an AO has multiple locations/ZIPs, a drive can be associated with that AO
through any of those locations.

The F3 API key must be supplied through the F3_API_KEY environment variable.
"""

from __future__ import annotations

import json
import os
import re
import time
from collections import defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path
from dotenv import load_dotenv


import requests
from selenium import webdriver
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from blooddrivedata import (
    F3_API_URL,
    F3_BOUNDING_BOX,
    OUTPUT_DIR,
    SEARCH_DAYS,
)


BLOODWORKS_URL = "https://donate.bloodworksnw.org/donor/schedules/zip"

load_dotenv()

def fetch_f3_locations() -> list[dict]:
    """Fetch active F3 locations from the configured bounding box."""
    api_key = ""
    if os.getenv("DEBUG") == "True":
        print('1 os.getenv:', os.getenv("DEBUG"), os.getenv("F3NATION_API_KEY"))
        api_key = os.getenv("F3NATION_API_KEY")
    else:    
        print('2 os.getenv:', os.getenv("DEBUG"), os.environ.get("F3_API_KEY"))
        api_key = os.environ.get("F3_API_KEY")
    if not api_key:
        raise RuntimeError(
            "F3_API_KEY is not set. Add it as a GitHub Actions repository secret."
        )

    response = requests.get(
        F3_API_URL,
        params=F3_BOUNDING_BOX,
        headers={
            "client": "scalar-api",
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json",
        },
        timeout=30,
    )
    response.raise_for_status()

    payload = response.json()
    locations = payload.get("locations", [])

    # locationName is the AO name in the supplied F3 map data.
    # Ignore inactive locations and records without an AO or ZIP.
    active = []
    for location in locations:
        if not location.get("isActive"):
            continue

        ao = (location.get("locationName") or "").strip()
        zip_code = (
            str(location.get("addressZip") or "").strip()
            or str((location.get("meta") or {}).get("postalCode") or "").strip()
        )

        if not ao or not re.fullmatch(r"\d{5}", zip_code):
            continue

        active.append(
            {
                "id": location.get("id"),
                "ao": ao,
                "zip_code": zip_code,
                "location_name": location.get("locationName"),
                "address": " ".join(
                    x for x in [
                        location.get("addressStreet"),
                        location.get("addressStreet2"),
                        location.get("addressCity"),
                        location.get("addressState"),
                        location.get("addressZip"),
                    ]
                    if x
                ),
                "latitude": location.get("latitude"),
                "longitude": location.get("longitude"),
            }
        )

    return active


def build_zip_to_aos(locations: list[dict]) -> dict[str, list[str]]:
    """Build ZIP -> AOs from the F3 location data."""
    mapping = defaultdict(set)
    for location in locations:
        mapping[location["zip_code"]].add(location["ao"])

    return {
        zip_code: sorted(aos)
        for zip_code, aos in sorted(mapping.items())
    }


def make_driver() -> webdriver.Chrome:
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1440,1200")
    return webdriver.Chrome(options=options)


def parse_drive_date(value: str) -> str | None:
    """Return an ISO date for the Bloodworks display text when possible."""
    value = " ".join(value.replace("\n", " ").split())

    patterns = [
        r"\b\d{1,2}/\d{1,2}/\d{4}\b",
        r"\b[A-Za-z]{3,9}\s+\d{1,2},\s+\d{4}\b",
    ]

    for pattern in patterns:
        match = re.search(pattern, value)
        if not match:
            continue

        raw = match.group(0)
        for fmt in ("%m/%d/%Y", "%B %d, %Y", "%b %d, %Y"):
            try:
                return datetime.strptime(raw, fmt).date().isoformat()
            except ValueError:
                pass

    return None


def search_zip(driver, zip_code: str, end_date: str) -> list[dict]:
    wait = WebDriverWait(
        driver,
        30,
        ignored_exceptions=(NoSuchElementException, StaleElementReferenceException),
    )

    driver.get(BLOODWORKS_URL)

    zipcode_box = wait.until(
        EC.presence_of_element_located((By.NAME, "zipcode"))
    )
    zipcode_box.click()
    zipcode_box.send_keys(Keys.HOME)
    zipcode_box.send_keys(zip_code)

    # Preserve the original scraper's search-radius behavior.
    slider = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[role="slider"]'))
    )
    print("slider:", slider)
    distance_label = wait.until(
        EC.presence_of_element_located((By.ID, "distance-label"))
    )
    for _ in range(30):
        miles = distance_label.text[:distance_label.text.find(" ")].strip()
        # writerPrediction[writerPrediction.find(" ")+1:writerPrediction.find("-")].strip()
        print('distance label: ', miles)
        if int(miles) == 5:
            break
        slider.send_keys(Keys.ARROW_LEFT)
        time.sleep(0.05)

    wait.until(
        lambda d: int(miles) == 5
    )
    # driver.execute_script("""
    #     arguments[0].value = 5;
    #     arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
    #     arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
    # """, slider)

    print(f"Searching ZIP code: {zip_code} with end date: {end_date} at distance: {distance_label.text.strip()}")

    end_date_box = wait.until(
        EC.presence_of_element_located((By.NAME, "end_date"))
    )
    end_date_box.click()
    end_date_box.send_keys(Keys.CONTROL + "a")
    end_date_box.send_keys(end_date)
    end_date_box.send_keys(Keys.TAB)

    driver.find_element(By.ID, "search").click()

    wait.until(EC.presence_of_element_located((By.ID, "item_table")))

    rows_out = []

    while True:
        table = wait.until(
            EC.visibility_of_element_located((By.ID, "item_table"))
        )
        rows = table.find_elements(By.TAG_NAME, "tr")

        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) < 5:
                continue

            drive_name = cols[0].text.strip()
            drive_date_time = " ".join(cols[3].text.split())

            try:
                drive_link = cols[4].find_element(
                    By.TAG_NAME, "a"
                ).get_attribute("href")
            except NoSuchElementException:
                drive_link = ""

            if drive_name and drive_link:
                rows_out.append(
                    {
                        "search_zip": zip_code,
                        "drive_name": drive_name,
                        "date_time": drive_date_time,
                        "date": parse_drive_date(drive_date_time),
                        "url": drive_link,
                    }
                )

        try:
            next_button = driver.find_element(By.ID, "item_table_next")
            classes = next_button.get_attribute("class") or ""

            if "disabled" in classes:
                break
            
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_button)

            next_link = next_button.find_element(By.TAG_NAME, "a")
            next_link.click()
            time.sleep(0.5)

        except NoSuchElementException:
            break

    return rows_out


def deduplicate(rows: list[dict], zip_to_aos: dict[str, list[str]]) -> list[dict]:
    """Merge duplicate drives returned by searches around multiple F3 ZIPs."""
    grouped = {}

    for row in rows:
        key = row["url"] or (row["drive_name"], row["date_time"])

        if key not in grouped:
            grouped[key] = {
                "drive_name": row["drive_name"],
                "date_time": row["date_time"],
                "date": row["date"],
                "url": row["url"],
                "zip_codes": set(),
                "aos": set(),
            }

        grouped[key]["zip_codes"].add(row["search_zip"])
        grouped[key]["aos"].update(zip_to_aos.get(row["search_zip"], []))

        if not grouped[key]["date"]:
            grouped[key]["date"] = row["date"]

    result = []
    for item in grouped.values():
        result.append(
            {
                "drive_name": item["drive_name"],
                "date_time": item["date_time"],
                "date": item["date"],
                "url": item["url"],
                "zip_codes": sorted(item["zip_codes"]),
                "aos": sorted(item["aos"]),
            }
        )

    return sorted(
        result,
        key=lambda x: (
            x["date"] or "9999-12-31",
            x["date_time"],
            x["drive_name"],
        ),
    )


def main():
    today = date.today()
    end_date = today + timedelta(days=SEARCH_DAYS)
    end_date_string = f"{end_date.month}/{end_date.day}/{end_date.year}"

    print("Fetching active F3 locations...")
    locations = fetch_f3_locations()

    if not locations:
        raise RuntimeError("F3 API returned no active locations with ZIP codes.")

    zip_to_aos = build_zip_to_aos(locations)

    print(f"Found {len(locations)} active F3 locations.")
    print(f"Searching {len(zip_to_aos)} unique ZIP codes.")
    print(f"Searching Bloodworks through {end_date_string}.")

    driver = make_driver()
    all_rows = []

    try:
        for zip_code in zip_to_aos:
            print(
                f"Searching ZIP {zip_code} "
                f"({', '.join(zip_to_aos[zip_code])})"
            )
            try:
                all_rows.extend(
                    search_zip(driver, zip_code, end_date_string)
                )
            except Exception as exc:
                # Don't lose the entire monthly run because one ZIP failed.
                print(f"ERROR searching {zip_code}: {exc}")
    finally:
        driver.quit()

    drives = deduplicate(all_rows, zip_to_aos)

    output = {
        "generated_at": today.isoformat(),
        "search_through": end_date.isoformat(),
        "location_count": len(locations),
        "zip_count": len(zip_to_aos),
        "drive_count": len(drives),
        "locations": locations,
        "drives": drives,
    }

    output_path = Path(OUTPUT_DIR) / "blood-drives.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2),
        encoding="utf-8",
    )

    print(f"Wrote {len(drives)} unique drives to {output_path}")


if __name__ == "__main__":
    main()
