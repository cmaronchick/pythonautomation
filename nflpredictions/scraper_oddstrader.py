# Python script for web scraping to extract data from a website
import sys, re, traceback
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Setup the Chrome WebDriver

imageTable = {
    'Entity_1569032072644.png': 'Steelers',
    'https://images.jifo.co/21540751_1589234309546.png': 'Chiefs',
    'https://images.jifo.co/21540751_1589234633468.png': 'Ravens',
    'Entity_1569032081184.png': 'Seahawks',
    'https://images.jifo.co/21540751_1589234284171.png': 'Chargers', #https://images.jifo.co/21540751_1589234284171.png
    'Entity_1569032070001.png': 'Patriots',
    'Entity_1569032074570.png': 'Broncos',
    'Entity_1569032071904.png': 'Bengals',
    'Entity_1599884617535.png': 'Rams',
    'Entity_1569032080155.png': 'Cardinals',
    'Entity_1569032074153.png': 'Titans',
    'Entity_1569032073772.png': 'Jaguars',
    'https://images.jifo.co/21540751_1589235745366.png': 'Buccaneers',
    'Entity_1569032073400.png': 'Colts',
    'Entity_1569032075665.png': 'Raiders',
    'Entity_1569032079464.png': 'Saints',
    'https://images.jifo.co/21540751_1589234933718.png': 'Bills',
    'https://images.jifo.co/21540751_1589235782787.png': 'Eagles',
    'Entity_1569032072269.png': 'Browns',
    'Entity_1569032069679.png': 'Dolphins',
    'https://images.jifo.co/21540751_1589235378659.png': 'Vikings',
    'Entity_1569032078079.png': 'Packers',
    'Entity_1569032078724.png': 'Falcons',
    'https://images.jifo.co/21540751_1652361392787.png': 'Commanders',
    'Entity_1569032077717.png': 'Lions'
}

articleTable = [
    "https://www.oddstrader.com/nfl/picks/"
    
]

chrome_driver_path = './chromedriver'

service = Service(chrome_driver_path)
def fetch_oddstrader_data(weeknum, weboptions):
    print('fetch_oddstrader_data:')
    
    driver = webdriver.Chrome(options=weboptions)
    driver.set_page_load_timeout(20)
    oddstraderrows = []
    try:
        for url in articleTable:
            print('url: ', url)
            # oddstrader formatting
            driver.get(url)
            wait = WebDriverWait(driver, timeout=5)
            writersText = []
            upcomingGamesTable = wait.until(EC.presence_of_element_located(
                (By.XPATH, "//*[contains(@class, 'leagueGroup')]")
            )) # //*[@id="PageHandler"]/div/div[1]/div/section/div[1]/div[3]/div/a[2]/div[2]/div[1]/div
            # original_window = driver.current_window_handle
            # windowhandles = len(driver.window_handles)
            # resultsTable = driver.find_elements_by_xpath("//*[contains(text(), " + writer['searchTerm'] + ")]")
            
            # articleBody = driver.find_element(By.TAG_NAME, "article")          
            print('leagueGroup found')  
            upcomingGames = upcomingGamesTable.find_elements(By.XPATH, "//div[contains(@class, 'participantsWrapper')]")
            print(len(upcomingGames))
            columnIndex = 0
            for game in upcomingGames:
                try:
                    matchup = None
                    teamsDiv = None
                    matchup = game.find_element(By.TAG_NAME, "div") #"//div[contains(@class, 'participantsWrapper')]"
                    teamsDiv = matchup.find_elements(By.XPATH, "./div[contains(@class, 'participant')]") # "//div[contains(@class, 'participant')]"
                    # driver.find_element(By.CSS_SELECTOR,          "div[class^='dd algo algo-sr']")
                    print(len(teamsDiv))
                    awaySpans = teamsDiv[0].find_elements(By.TAG_NAME,"span")
                    awayTeam = awaySpans[0].text
                    awayTeamScore = awaySpans[len(awaySpans)-1].text
                    if awayTeamScore != '':
                        awayTeamScore = int(awayTeamScore)
                    print('awayTeam: ', awayTeam, awayTeamScore)
                    homeSpans = teamsDiv[1].find_elements(By.TAG_NAME, "span") 
                    homeTeam = homeSpans[0].text
                    homeTeamScore = homeSpans[len(homeSpans)-1].text
                    if homeTeamScore != '':
                        homeTeamScore = int(homeTeamScore)
                    print('homeTeam: ', homeTeam, homeTeamScore)
                    oddstraderrows.append(['oddstrader',awayTeam, awayTeamScore, homeTeam, homeTeamScore])
                except Exception as e:
                    print('Exception: ', e)
                columnIndex = columnIndex + 1
        print('oddstraderrows:', oddstraderrows)
        driver.quit()
        return oddstraderrows
    except Exception as e:
        print('Exception:', e)
        traceback.print_exc()
        driver.quit()
        return oddstraderrows


def main(weeknum):
    html_content = fetch_oddstrader_data(weeknum) #'https://tallysight.com/new/widget/staff-picks/usa-today-sports/nfl/event:2024-25-week-17/default:ml/types:ml,ats/extras:condensed/performances:bboverall,overall?id=5fef16ef-7f0c-41e5-81c9-a000636d9d0c'
    if html_content:
        print(html_content)
    else:
        print("Failed to retrieve data")

if __name__ == "__main__":
    weeknum = sys.argv[0]
    main(weeknum)
