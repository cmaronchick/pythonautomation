import csv
import re
import sys
import traceback

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait


chrome_driver_path = './chromedriver'
service = Service(chrome_driver_path)
DEFAULT_URL = "https://www.nfl.com/news/nfl-picks-week-1-2026-nfl-season"

CSV_COLUMNS = [
    "author",
    "winning team",
    "winning score",
    "losing team",
    "losing score",
]


def make_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1440,1200")

    # service = Service(CHROME_DRIVER_PATH)
    return webdriver.Chrome(options=options)


def get_game_teams(section):
    """
    Get the two team links immediately preceding the AUTHOR PICKS section.
    On the current NFL page, those are the matchup teams for that section.
    """
    links = section.find_elements(
        By.XPATH,
        "preceding::a[contains(@href, '/teams/') and normalize-space()]"
    )

    # The nearest two team links are the matchup teams.
    teams = []
    for link in reversed(links):
        name = link.text.strip()
        if name and name not in teams:
            teams.insert(0, name)
        if len(teams) == 2:
            break

    if len(teams) != 2:
        raise ValueError(f"Could not determine matchup teams: {teams}")

    return teams[0], teams[1]


def get_pick_teams(section):
    """
    The current NFL markup puts the selected team in the pick image's alt text:
        Image: Carolina Panthers

    Return the picked teams in the same order as the five predictions.
    """
    picked_teams = []

    images = section.find_elements(
        By.TAG_NAME,
        "img"
    ) #".//img[starts-with(@alt, 'Image:')]"
    print('images: ', len(images))

    for image in images:
        alt = (image.get_attribute("alt") or "").strip()
        print('alt: ', alt)
        if alt is not None:
            team = alt.strip()
            if team:
                picked_teams.append(team)

    return picked_teams


def parse_predictions(section):
    """
    Parse the five 'Predicted score: NN-NN' entries directly from the
    rendered section text. This is considerably more reliable than relying
    on the position of spans, which is what the old scraper did.
    """
    text = section.text

    matches = re.findall(
        r"Predicted score:\s*(\d+)\s*-\s*(\d+)",
        text,
        flags=re.IGNORECASE,
    )

    return [(int(winner), int(loser)) for winner, loser in matches]


def parse_authors(section, prediction_count):
    """
    On the current page each pick is rendered approximately as:

        Author Name
        Image: Team
        24-23
        Predicted score: 24-23

    Selenium's element.text does not reliably include image alt text, but it
    does include the author and score lines. We therefore find the line
    immediately before each raw score/predicted-score pair.
    """
    lines = [line.strip() for line in section.text.splitlines() if line.strip()]

    authors = []

    for i, line in enumerate(lines):
        if not re.fullmatch(r"\d+\s*-\s*\d+", line):
            continue

        # A raw score line is immediately followed by "Predicted score:".
        if i + 1 >= len(lines):
            continue

        if not re.match(r"^Predicted score:", lines[i + 1], re.IGNORECASE):
            continue

        # The author is normally the closest non-score line above the score.
        author = None
        for j in range(i - 1, max(-1, i - 5), -1):
            candidate = lines[j]

            if re.fullmatch(r"\d+\s*-\s*\d+", candidate):
                continue

            if re.match(r"^Predicted score:", candidate, re.IGNORECASE):
                continue

            if candidate.lower() == "image":
                continue

            if candidate.startswith("Image:"):
                continue

            if candidate:
                author = candidate
                break

        if author:
            authors.append(author)

    if len(authors) != prediction_count:
        raise ValueError(
            f"Found {len(authors)} authors for {prediction_count} predictions"
        )

    return authors


def normalize_team_name(team):
    """
    Handle minor display-name differences between the matchup link and
    image alt text.
    """
    return re.sub(r"\s+", " ", team.strip()).lower()


def fetch_nfl_data(url, make_driver_func=make_driver):
    driver = make_driver_func()
    driver.set_page_load_timeout(35)

    nflrows = []

    try:
        driver.get(url)

        wait = WebDriverWait(driver, timeout=15)
        article_body = wait.until(
            lambda d: d.find_element(By.ID, "main-content")
        )
        wait.until(lambda d: article_body.is_displayed())

        # This is the important change from the old scraper:
        # don't assume every span in AUTHOR PICKS is an author and don't
        # assume the prediction index corresponds to a span index.
        sections = article_body.find_elements(
            By.XPATH,
            ".//section[.//h2[normalize-space()='AUTHOR PICKS']]"
        )

        print(f"AUTHOR PICKS sections found: {len(sections)}")

        for section_index, section in enumerate(sections, start=1):
            try:
                away_team, home_team = get_game_teams(section)
                predictions = parse_predictions(section)
                picked_teams = get_pick_teams(section)

                if len(predictions) != 5:
                    raise ValueError(
                        f"Expected 5 predictions, found {len(predictions)}"
                    )

                if len(picked_teams) != 5:
                    raise ValueError(
                        f"Expected 5 picked teams, found {len(picked_teams)}"
                    )

                authors = parse_authors(section, len(predictions))

                print(
                    f"Game {section_index}: "
                    f"{away_team} vs {home_team} | "
                    f"{len(predictions)} predictions"
                )

                for author, picked_team, (winning_score, losing_score) in zip(
                    authors, picked_teams, predictions
                ):
                    # The image identifies the team the author picked to win.
                    if normalize_team_name(picked_team) == normalize_team_name(away_team):
                        winning_team = away_team
                        losing_team = home_team
                    elif normalize_team_name(picked_team) == normalize_team_name(home_team):
                        winning_team = home_team
                        losing_team = away_team
                    else:
                        raise ValueError(
                            f"Picked team '{picked_team}' does not match "
                            f"'{away_team}' or '{home_team}'"
                        )

                    nflrows.append([
                        author,
                        winning_team,
                        winning_score,
                        losing_team,
                        losing_score,
                    ])

            except Exception as exc:
                print(
                    f"Could not parse game section {section_index}: {exc}"
                )

        return nflrows

    except Exception as exc:
        print("NFL exception:", exc)
        traceback.print_exc()
        return nflrows

    finally:
        driver.quit()


def write_csv(rows, weeknum):
    filename = f"nfl_picks_week_{weeknum}.csv"

    with open(filename, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(CSV_COLUMNS)
        writer.writerows(rows)

    return filename


def main(weeknum):
    # Keep the URL format flexible so the same scraper can be used for
    # future weeks in the 2026 season.
    url = f"https://www.nfl.com/news/nfl-picks-week-{weeknum}-2026-nfl-season"

    rows = fetch_nfl_data(url)

    if not rows:
        print("Failed to retrieve data")
        return

    filename = write_csv(rows, weeknum)

    print(f"\nWrote {len(rows)} predictions to {filename}")
    print("author | winning team | winning score | losing team | losing score")

    for row in rows:
        print(" | ".join(map(str, row)))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scraper_nfl.py <week_number>")
        sys.exit(1)

    main(int(sys.argv[1]))
