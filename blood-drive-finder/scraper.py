"""Scrape Bloodworks Northwest drives for the configured AO ZIP codes.

The scraper intentionally keeps the Bloodworks interaction close to the original
script: Selenium is used because the search form/table is rendered interactively.
"""

from __future__ import annotations

import json
import re
import time
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path

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

from blooddrivedata import AO_ZIPCODES, OUTPUT_DIR, SEARCH_DAYS

URL = "https://donate.bloodworksnw.org/donor/schedules/zip"


def parse_date_time(value: str) -> tuple[str, str]:
    """Best-effort split of the site's combined date/time text."""
    value = " ".join(value.replace("\n", " ").split())
    # Keep the raw display value too; parsing is only for sorting.
    return value, ""


def make_driver() -> webdriver.Chrome:
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1440,1200")
    return webdriver.Chrome(options=options)


def search_zip(driver, zip_code: int, end_date: str) -> list[dict]:
    wait = WebDriverWait(
        driver,
        30,
        ignored_exceptions=(NoSuchElementException, StaleElementReferenceException),
    )

    driver.get(URL)

    zipcode_box = wait.until(EC.presence_of_element_located((By.NAME, "zipcode")))
    zipcode_box.click()
    zipcode_box.send_keys(Keys.HOME)
    zipcode_box.send_keys(str(zip_code))

    # Match the original script's behavior: move the distance slider left.
    slider = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "slider-handle")))
    for _ in range(22):
        slider.send_keys(Keys.ARROW_LEFT)

    end_date_box = wait.until(EC.presence_of_element_located((By.NAME, "end_date")))
    end_date_box.click()
    end_date_box.send_keys(Keys.CONTROL + "a")
    end_date_box.send_keys(end_date)
    end_date_box.send_keys(Keys.TAB)

    driver.find_element(By.ID, "search").click()

    wait.until(EC.presence_of_element_located((By.ID, "item_table")))

    rows_out = []
    while True:
        table = wait.until(EC.visibility_of_element_located((By.ID, "item_table")))
        rows = table.find_elements(By.TAG_NAME, "tr")

        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) < 5:
                continue

            drive_name = cols[0].text.strip()
            drive_date_time = " ".join(cols[3].text.split())

            try:
                link = cols[4].find_element(By.TAG_NAME, "a").get_attribute("href")
            except NoSuchElementException:
                link = ""

            if drive_name and link:
                rows_out.append(
                    {
                        "zip_code": zip_code,
                        "drive_name": drive_name,
                        "date_time": drive_date_time,
                        "url": link,
                    }
                )

        # Stop when the next-page button is disabled.
        try:
            next_button = driver.find_element(By.ID, "item_table_next")
            classes = next_button.get_attribute("class") or ""
            if "disabled" in classes:
                break

            next_link = next_button.find_element(By.TAG_NAME, "a")
            next_link.click()
            time.sleep(0.5)
        except NoSuchElementException:
            break

    return rows_out


def deduplicate(rows: list[dict]) -> list[dict]:
    """Merge duplicate drives found from multiple ZIP-code searches."""
    grouped = {}

    for row in rows:
        key = row["url"] or (
            row["drive_name"],
            row["date_time"],
        )

        if key not in grouped:
            grouped[key] = {
                "drive_name": row["drive_name"],
                "date_time": row["date_time"],
                "url": row["url"],
                "zip_codes": set(),
                "aos": set(),
            }

        grouped[key]["zip_codes"].add(row["zip_code"])

    # Map every search ZIP back to its AO(s).
    zip_to_aos = defaultdict(list)
    for ao, zip_code in AO_ZIPCODES.items():
        zip_to_aos[zip_code].append(ao)

    result = []
    for item in grouped.values():
        for zip_code in item["zip_codes"]:
            item["aos"].update(zip_to_aos[zip_code])

        result.append(
            {
                "drive_name": item["drive_name"],
                "date_time": item["date_time"],
                "url": item["url"],
                "zip_codes": sorted(item["zip_codes"]),
                "aos": sorted(item["aos"]),
            }
        )

    return sorted(result, key=lambda x: (x["date_time"], x["drive_name"]))


def main():
    today = date.today()
    end_date = today + timedelta(days=SEARCH_DAYS)
    end_date_string = f"{end_date.month}/{end_date.day}/{end_date.year}"

    print(f"Searching through {end_date_string}...")

    driver = make_driver()
    all_rows = []

    try:
        # The original script searched each ZIP independently. We retain that behavior.
        for zip_code in sorted(set(AO_ZIPCODES.values())):
            print(f"Searching ZIP {zip_code}")
            try:
                all_rows.extend(search_zip(driver, zip_code, end_date_string))
            except Exception as exc:
                print(f"ERROR searching {zip_code}: {exc}")
    finally:
        driver.quit()

    drives = deduplicate(all_rows)

    output = {
        "generated_at": today.isoformat(),
        "search_through": end_date.isoformat(),
        "drive_count": len(drives),
        "drives": drives,
    }

    output_path = Path(OUTPUT_DIR) / "blood-drives.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output, indent=2), encoding="utf-8")

    print(f"Wrote {len(drives)} unique drives to {output_path}")


if __name__ == "__main__":
    main()
