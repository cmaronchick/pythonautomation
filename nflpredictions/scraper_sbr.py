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

def fetch_sbr_data(weeknum, url, weboptions):
    driver = webdriver.Chrome(options=weboptions)
    try: 
        # nfl formatting
        sbrrows = []
        driver.get(url) #'https://www.nfl.com/news/week-' + str(weeknum) + '-nfl-picks-2024-nfl-season'
        wait = WebDriverWait(driver, timeout=2)
        # driver.implicitly_wait(10)
        # resultsTable = driver.find_elements_by_xpath("//*[contains(text(), " + writer['searchTerm'] + ")]")
        articleBody = driver.find_element(By.CLASS_NAME, "container")
        wait.until(lambda d : articleBody.is_displayed())
        matchups = driver.find_elements(By.CLASS_NAME, "table")
        print('nfltables:', len(matchups))
        tableIndex = 0
        gamesObject = {}
        for matchup in matchups:
            body = matchup.find_element(By.TAG_NAME, "tbody")
            rows = body.find_elements(By.TAG_NAME, "tr")
            print('sbr rows:', len(rows))
            if len(rows) > 0:
                awayRow = rows[0]
                awayRowCols = awayRow.find_elements(By.TAG_NAME, "td")
                homeRow = rows[1]
                homeRowCols = homeRow.find_elements(By.TAG_NAME, "td")
                print('sbr cols: ', len(awayRowCols), len(homeRowCols))
                if len(awayRowCols) >0 and len(homeRowCols) > 0:
                    try: 
                        awayTeam = awayRowCols[0].text
                        awayScore = int(awayRowCols[len(awayRowCols)-1].text)
                        homeTeam = homeRowCols[0].text
                        homeScore = int(homeRowCols[len(awayRowCols)-1].text)
                        if awayScore > homeScore:
                            winningTeam = awayTeam
                            winningScore = awayScore
                            losingTeam = homeTeam
                            losingScore = homeScore
                        else:
                            winningTeam = homeTeam
                            winningScore = homeScore
                            losingTeam = awayTeam
                            losingScore = awayScore
                        sbrrows.append(['SBR',winningTeam, winningScore, losingTeam, losingScore]) 
                    except Exception as e:
                        print('sbr table exception: ', e)

        # print(sbrrows)
        driver.close()
        return sbrrows
    except Exception as e:
        print('sbr exception: ', e)
        driver.close()
        return sbrrows

def main(weeknum):
    html_content = fetch_sbr_data(weeknum)
    if html_content:
        print(html_content)
    else:
        print("Failed to retrieve data")

if __name__ == "__main__":
    main()