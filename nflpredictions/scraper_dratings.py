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
    "https://www.dratings.com/predictor/nfl-football-predictions/#scroll-upcoming",
    "https://www.dratings.com/predictor/nfl-football-predictions/upcoming/4#scroll-upcoming",
    "https://www.dratings.com/predictor/nfl-football-predictions/upcoming/5#scroll-upcoming"
    
]

chrome_driver_path = './chromedriver'

service = Service(chrome_driver_path)
# weboptions = webdriver.ChromeOptions()
# weboptions.accept_insecure_certs = True
# weboptions.add_argument('--ignore-certificate-errors')
# weboptions.add_argument('disable-notifications')
# weboptions.add_argument("--log-level=3")
# weboptions.page_load_strategy = 'eager'
def fetch_dratings_data(weeknum, weboptions):
    driver = webdriver.Chrome(options=weboptions)
    driver.set_page_load_timeout(20)
    print('fetch_dratings_data:')
    dratingsrows = []
    try:
        for url in articleTable:
            print('url: ', url)
            # dratings formatting
            driver.get(url)
            wait = WebDriverWait(driver, timeout=5)
            writersText = []
            upcomingGames = wait.until(EC.presence_of_element_located((By.ID, "scroll-upcoming")))
            # original_window = driver.current_window_handle
            # windowhandles = len(driver.window_handles)
            # resultsTable = driver.find_elements_by_xpath("//*[contains(text(), " + writer['searchTerm'] + ")]")
            
            # articleBody = driver.find_element(By.TAG_NAME, "article")            
            table = wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
            writers = table.find_elements(By.TAG_NAME, "tr")
            
            # use for tallysight URL
            tableBody = table.find_element(By.TAG_NAME, "tbody")
            tableRows = tableBody.find_elements(By.TAG_NAME, "tr")
                # specialOffer = driver.find_elements(By.CSS_SELECTOR, "iframe[title='Special offer']")
                # if len(specialOffer) > 0:
                #     # articleBody.send_keys(Keys.ESCAPE)
                #     driver.switch_to
            print(len(tableRows))
            for tableRow in tableRows:
                columnIndex = 0
                columns = tableRow.find_elements(By.TAG_NAME, "td")
                awayTeam = ""
                homeTeam = ""
                for column in columns:
                    if columnIndex == 1:
                        teamSpans = column.find_elements(By.TAG_NAME, "span")
                        awayTeam = teamSpans[0].find_element(By.TAG_NAME,'a').text
                        homeTeam = teamSpans[2].find_element(By.TAG_NAME,'a').text
                        print(awayTeam, homeTeam)
                    else:
                        if columnIndex == 6:
                            spans = column.text.split("\n")
                            print('spans: ', spans)
                            awayTeamScore = round(float(spans[0]))
                            homeTeamScore = round(float(spans[1]))                        
                            # print('author:', 'DRatings', awayTeam, awayTeamScore, homeTeam, homeTeamScore)
                            dratingsrows.append(['DRatings',awayTeam, awayTeamScore, homeTeam, homeTeamScore])
                    columnIndex = columnIndex + 1
        print('dratingsrows:', dratingsrows)
        driver.quit()
        return dratingsrows
    except Exception as e:
        print('Exception:', e)
        traceback.print_exc()
        driver.quit()
        return dratingsrows


def main(weeknum):
    html_content = fetch_dratings_data(weeknum) #'https://tallysight.com/new/widget/staff-picks/usa-today-sports/nfl/event:2024-25-week-17/default:ml/types:ml,ats/extras:condensed/performances:bboverall,overall?id=5fef16ef-7f0c-41e5-81c9-a000636d9d0c'
    if html_content:
        print(html_content)
    else:
        print("Failed to retrieve data")

if __name__ == "__main__":
    weeknum = sys.argv[0]
    main(weeknum)
