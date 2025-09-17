import requests, sys, datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_driver_path = './chromedriver'

service = Service(chrome_driver_path)
# weboptions = webdriver.ChromeOptions()
# weboptions.accept_insecure_certs = True

def fetch_nfl_data(weeknum, url, weboptions):
    driver = webdriver.Chrome(options=weboptions)
    try: 
        # nfl formatting
        nflrows = []
        driver.get(url) #'https://www.nfl.com/news/week-' + str(weeknum) + '-nfl-picks-2024-nfl-season'
        wait = WebDriverWait(driver, timeout=2)
        # driver.implicitly_wait(10)
        # resultsTable = driver.find_elements_by_xpath("//*[contains(text(), " + writer['searchTerm'] + ")]")
        articleBody = driver.find_element(By.CLASS_NAME, "nfl-c-article__body")
        wait.until(lambda d : articleBody.is_displayed())
        tables = driver.find_elements(By.CLASS_NAME, "d3-o-table--detailed")
        print('nfltables:', len(tables))
        tableIndex = 0
        gamesObject = {}
        matchups = driver.find_elements(By.CLASS_NAME, "nfl-o-ranked-item--side-by-side")
        for matchup in matchups:
            awayTeam = matchup.find_elements(By.CLASS_NAME, "nfl-o-ranked-item__title")[0].text
            awayMascot = awayTeam[awayTeam.rfind(" "):].strip()
            homeTeam = matchup.find_elements(By.CLASS_NAME, "nfl-o-ranked-item__title")[1].text
            homeMascot = homeTeam[homeTeam.rfind(" "):].strip()
            gamesObject[homeMascot.lower()] = {
                "awayTeam": awayMascot,
                "homeTeam": homeMascot
            }
            gamesObject[awayMascot.lower()] = {
                "awayTeam": awayMascot,
                "homeTeam": homeMascot
            }
        # print(gamesObject)
        for table in tables:
            if tableIndex > 0: 
                writersText = []
                writerIndex = 0
                writers = table.find_elements(By.TAG_NAME, "th")
                winningTeam = None
                losingTeam = None
                for writer in writers:
                    writersText.append({ "name": writer.text + "NFL", "prediction": "", "index": writerIndex})
                    writerIndex = writerIndex + 1
                predictions = table.find_elements(By.TAG_NAME, "td")
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
        driver.close()
        return nflrows
    except Exception as e:
        print('nfl exception: ', e)
        driver.close()
        return nflrows

def main(weeknum):
    html_content = fetch_nfl_data(weeknum)
    if html_content:
        print(html_content)
    else:
        print("Failed to retrieve data")

if __name__ == "__main__":
    main()