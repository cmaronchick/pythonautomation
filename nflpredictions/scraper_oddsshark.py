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
    "https://www.oddsshark.com/nfl/computer-picks"
    
]

chrome_driver_path = './chromedriver'

service = Service(chrome_driver_path)
# weboptions = webdriver.ChromeOptions()
# weboptions.accept_insecure_certs = True
# weboptions.add_argument('--ignore-certificate-errors')
# weboptions.add_argument('disable-notifications')
# weboptions.page_load_strategy = 'eager'
def fetch_oddsshark_data(weeknum, weboptions):
    
    driver = webdriver.Chrome(options=weboptions)
    print('fetch_dratings_data:')
    oddssharkrows = []
    try:
        for url in articleTable:
            print('url: ', url)
            # dratings formatting
            driver.get(url)
            wait = WebDriverWait(driver, timeout=2)
            driver.implicitly_wait(3)
            writersText = []
            gamesDiv = driver.find_element(By.CLASS_NAME, 'computer-picks-content')
            wait.until(lambda d : gamesDiv.is_displayed())
            upcomingGames = gamesDiv.find_elements(By.CLASS_NAME, "predicted-score")
            for game in upcomingGames:
                
                teams = game.find_elements(By.CLASS_NAME, 'team-shortname')
                scores = game.find_elements(By.CLASS_NAME, 'highlighted-text')
                awayTeam = teams[0].text
                homeTeam = teams[1].text
                if scores[1].text == '-' or scores[3].text == '-':
                    continue
                awayTeamScore = round(float(scores[1].text))
                homeTeamScore = round(float(scores [3].text))
                print('awayTeam, awayTeamScore, homeTeam, homeTeamScore:', awayTeam, awayTeamScore, homeTeam, homeTeamScore)
                oddssharkrows.append(['oddsshark', awayTeam, awayTeamScore, homeTeam, homeTeamScore])
        print('dratingsrows:', oddssharkrows)
        driver.close()
        return oddssharkrows
    except Exception as e:
        print('Exception:', e)
        traceback.print_exc()
        driver.close()
        return oddssharkrows


def main(weeknum):
    html_content = fetch_oddsshark_data(weeknum) #'https://tallysight.com/new/widget/staff-picks/usa-today-sports/nfl/event:2024-25-week-17/default:ml/types:ml,ats/extras:condensed/performances:bboverall,overall?id=5fef16ef-7f0c-41e5-81c9-a000636d9d0c'
    if html_content:
        print(html_content)
    else:
        print("Failed to retrieve data")

if __name__ == "__main__":
    weeknum = sys.argv[0]
    main(weeknum)
