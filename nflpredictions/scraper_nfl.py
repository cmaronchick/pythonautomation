import traceback

import requests, sys, datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_driver_path = './chromedriver'

service = Service(chrome_driver_path)
# weboptions = webdriver.ChromeOptions()
# weboptions.accept_insecure_certs = True


weeknum = int(sys.argv[1])

def make_driver() -> webdriver.Chrome:
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1440,1200")
    return webdriver.Chrome(options=options)

def fetch_nfl_data(weeknum, url, make_driver):
    driver = make_driver() # webdriver.Chrome(options=weboptions)
    driver.set_page_load_timeout(35)
    try: 
        # nfl formatting
        nflrows = []
        driver.get(url if url is not None else 'https://www.nfl.com/news/nfl-picks-week-1-2026-nfl-season') #'https://www.nfl.com/news/week-' + str(weeknum) + '-nfl-picks-2024-nfl-season'
        wait = WebDriverWait(driver, timeout=10)
        # driver.implicitly_wait(10)
        # resultsTable = driver.find_elements_by_xpath("//*[contains(text(), " + writer['searchTerm'] + ")]")
        articleBody = driver.find_element(By.ID, "main-content")
        wait.until(lambda d : articleBody.is_displayed())
        # tables = driver.find_elements(By.CLASS_NAME, "d3-o-table--detailed")
        # print('nfltables:', len(tables))
        tableIndex = 0
        gamesObject = {}
        # matchups = driver.find_elements(By.CLASS_NAME, "nfl-o-ranked-item--side-by-side")
        # matchups = driver.find_elements(
        #    By.XPATH, "//section[.//h2[normalize-space()='Author Picks']]"
        # )

        # Finds each game block/container on the page
        # game_boxes = driver.find_elements(By.XPATH, "//div[contains(@class, 'nfl-c-matchup-strip') or contains(@class, 'game-center')]")

        # Alternatively, if targeting the specific block structure containing team links:
        matchups = articleBody.find_elements(By.XPATH, "//div[.//a[contains(@href, '/teams/')]]")
        print('matchups:', len(matchups))
        for matchup in matchups:
            matchupDivs = matchup.find_elements(By.CLASS_NAME, "body-1-sans")
            if matchupDivs is None or len(matchupDivs) == 0:
                print(matchup.text)
                continue
            awayTeam = matchup.find_elements(By.CLASS_NAME, "body-1-sans")[0].text
            awayMascot = awayTeam[awayTeam.rfind(" "):].strip()
            # print('awayMascot: ', awayMascot)
            homeTeam = matchup.find_elements(By.CLASS_NAME, "body-1-sans")[1].text
            homeMascot = homeTeam[homeTeam.rfind(" "):].strip()
            if gamesObject.get(homeMascot.lower()) is None:
                gamesObject[homeMascot.lower()] = {
                    "awayTeam": awayMascot,
                    "homeTeam": homeMascot
                }
            if gamesObject.get(awayMascot.lower()) is None:
                gamesObject[awayMascot.lower()] = {
                    "awayTeam": awayMascot,
                    "homeTeam": homeMascot
                }

        print(gamesObject)
        tables = driver.find_elements(
           By.XPATH, "//section[.//h2[text()='AUTHOR PICKS']]"
        )
        print('nfltables: ', len(tables))
        for table in tables:
            if tableIndex > 0: 
                writersText = []
                writerIndex = 0
                writers = table.find_elements(By.TAG_NAME, "span")
                winningTeam = None
                losingTeam = None
                print('writers:', len(writers))
                for writer in writers:
                    if writer.text != "":
                        print('writer: ', writer.text)
                        writersText.append({ "name": writer.text + "NFL", "prediction": "", "index": writerIndex})
                    writerIndex = writerIndex + 1
                predictions = table.find_elements(By.XPATH, ".//span[normalize-space()='Predicted score:']")
                print('predictions: ', len(predictions))
                for writerObj in writersText:
                    writerIndex = writerObj["index"]
                    author = writerObj["name"]
                    writerPrediction = predictions[writerIndex].text
                    winner = writerPrediction[:writerPrediction.find(" ")].strip()
                    winningScore = writerPrediction[writerPrediction.find(" ")+1:writerPrediction.find("-")].strip()
                    losingScore = writerPrediction[writerPrediction.rfind("-")+1:].strip()
                    if gamesObject[winner.lower()]["awayTeam"] == winner:
                        winningTeam = gamesObject[winner.lower()]["awayTeam"]
                        losingTeam = gamesObject[winner.lower()]["homeTeam"]
                    else:
                        winningTeam = gamesObject[winner.lower()]["homeTeam"]
                        losingTeam = gamesObject[winner.lower()]["awayTeam"]

                    nflrows.append([author,winningTeam, winningScore, losingTeam, losingScore]) 
            tableIndex = tableIndex + 1
        # print(nflrows)
        driver.quit()
        return nflrows
    except Exception as e:
        print('nfl exception: ', e,traceback.print_exc())
        driver.quit()
        return nflrows

def main(weeknum):
    html_content = fetch_nfl_data(weeknum, 'https://www.nfl.com/news/nfl-picks-week-1-2026-nfl-season', make_driver)
    if html_content:
        print(html_content)
    else:
        print("Failed to retrieve data")

if __name__ == "__main__":
    
    weeknum = int(sys.argv[1])
    main(weeknum)