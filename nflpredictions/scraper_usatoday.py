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
    'Entity_1569032072644.png': 'Pittsburgh Steelers',
    'Entity_1569032074922.png': 'Kansas City Chiefs',
    'Entity_1569032070684.png': 'Baltimore Ravens',
    'Entity_1569032081184.png': 'Seattle Seahawks',
    'Entity_1569032075269.png': 'Los Angeles Chargers',
    'Entity_1569032070001.png': 'New England Patriots',
    'Entity_1569032074570.png': 'Denver Broncos',
    'Entity_1569032071904.png': 'Cincinnati Bengals',
    'Entity_1599884617535.png': 'Los Angeles Rams',
    'Entity_1569032080155.png': 'Arizona Cardinals',
    'Entity_1569032074153.png': 'Tennessee Titans',
    'Entity_1569032073772.png': 'Jacksonville Jaguars',
    'Entity_1569032079814.png': 'Tampa Bay Buccaneers',
    'Entity_1569032073400.png': 'Indianapolis Colts',
    'Entity_1569032075665.png': 'Las Vegas Raiders',
    'Entity_1569032079464.png': 'New Orleans Saints',
    'Entity_1569032069354.png': 'Buffalo Bills',
    'Entity_1569032076658.png': 'Philadelphia Eagles',
    'Entity_1569032072269.png': 'Cleveland Browns',
    'Entity_1569032069679.png': 'Miami Dolphins',
    'Entity_1569032078418.png': 'Minnesota Vikings',
    'Entity_1569032078079.png': 'Green Bay Packers',
    'Entity_1569032078724.png': 'Atlanta Falcons',
    'washington-football-team.png': 'Washington Commanders',
    'Entity_1569032077717.png': 'Detroit Lions'
}

chrome_driver_path = './chromedriver'

service = Service(chrome_driver_path)
weboptions = webdriver.ChromeOptions()
weboptions.accept_insecure_certs = True
weboptions.add_argument('--ignore-certificate-errors')
weboptions.add_argument('disable-notifications')
driver = webdriver.Chrome(options=weboptions)
def fetch_usatoday_data(weeknum, url):
    print('fetch_usatoday_data:', url)
    usatodayrows = []
    try:
        # usatoday formatting
            
        driver.get(url)
        wait = WebDriverWait(driver, timeout=2)
        driver.implicitly_wait(3)
        writersText = []
        
        # original_window = driver.current_window_handle
        # windowhandles = len(driver.window_handles)
        # resultsTable = driver.find_elements_by_xpath("//*[contains(text(), " + writer['searchTerm'] + ")]")
        
        # articleBody = driver.find_element(By.TAG_NAME, "article")
        table = driver.find_element(By.TAG_NAME, "table")
        wait.until(lambda d : table.is_displayed())
        writers = table.find_elements(By.TAG_NAME, "th")
        
        writersText = []
        writerIndex = 0
        for writer in writers:
            if writerIndex > 0:
                writersText.append({ "name": re.sub(r'\s+', '', writer.text), "prediction": "", "index": writerIndex})
            writerIndex = writerIndex + 1
        
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
                if columnIndex == 0:
                    teamSpans = column.find_elements(By.TAG_NAME, "span")
                    awayTeam = teamSpans[0].text
                    homeTeam = teamSpans[1].text
                    print(awayTeam, homeTeam)
                else:
                    spans = column.find_elements(By.TAG_NAME, "span")
                    print(len(spans))
                    if len(spans) == 1:
                        print(spans[0].text)
                        continue
                    winningTeam = None
                    losingScore = None
                    losingTeam = None
                    winningTeam = spans[0].text.strip()
                    score = spans[1].text
                    winningScore = score[:score.find("-")].strip()
                    losingScore = score[score.rfind("-")+1:].strip()
                    if winningTeam == awayTeam:
                        losingTeam = homeTeam
                    else:
                        losingTeam = awayTeam
                    author = writersText[columnIndex-1]["name"]

                    
                    print('author:', author, winningTeam, winningScore, losingTeam, losingScore)
                    usatodayrows.append([author,winningTeam, winningScore, losingTeam, losingScore])
                columnIndex = columnIndex + 1

        # pickLinkIndex = 0
        # wait.until(lambda d : articleBody.is_displayed())
        # pickLinks = articleBody.find_elements(By.XPATH,'//a[contains(text(), " vs. ")]')    # pickLinks2 = driver.find_elements(By.XPATH, "/html/body/div[3]/main/article/div[5]/p[10]/a")
        # print('usatoday picklinks 37:', len(pickLinks))
        # while pickLinkIndex < len(pickLinks):
            
        #     popup = driver.find_elements(By.CLASS_NAME, "gnt_mol_xb")
        #     if len(popup) > 0:
        #         popup[0].click()
        #     pickLinks[pickLinkIndex].click()
        #     if len(driver.window_handles) > 1:
        #         driver.switch_to.window(driver.window_handles[len(driver.window_handles)-1])
        #     articleBody = driver.find_element(By.TAG_NAME, "article")
        #     wait.until(lambda d : articleBody.is_displayed())
        #     title = driver.find_element(By.TAG_NAME, "h1")
        #     wait.until(lambda d : title.is_displayed())
        #     headers = driver.find_elements(By.TAG_NAME, "h2")
        #     headerIndex = 0
        #     for header in headers:
        #         winnerScore = None
        #         winningTeam = None
        #         losingScore = None
        #         losingTeam = None
        #         if headerIndex > 1:
        #             separatorIndex = header.text.find(":")
        #             author = header.text[:separatorIndex].replace(" ","")
        #             winner = header.text[separatorIndex+2:header.text.find(",")].split(" ")
        #             winningTeam = winner[0]
        #             if len(winner) > 1:
        #                 winningScore = winner[1]
        #             loser = header.text[header.text.find(",")+2:].split(" ")
        #             losingTeam = loser[0]
        #             if len(loser) > 1:
        #                 losingScore = loser[1]
        #             print('author:', author, winningTeam, winningScore, losingTeam, losingScore)
        #             usatodayrows.append([author,winningTeam, winningScore, losingTeam, losingScore])                    
        #         headerIndex = headerIndex + 1
        #     pickLinkIndex = pickLinkIndex + 1 
        #     driver.get(url)
        #     popup = driver.find_elements(By.CLASS_NAME, "gnt_mol_xb")
        #     if len(popup) > 0:
        #         popup[0].click()
        #     articleBody = driver.find_element(By.TAG_NAME, "article")
        #     wait.until(lambda d : articleBody.is_displayed())

        #     pickLinks = articleBody.find_elements(By.XPATH,'//a[contains(text(), " vs. ")]')
        #     print('usatoday picklinks 80:', len(pickLinks))
        print('usatodayrows:', usatodayrows)
        return usatodayrows
    except Exception as e:
        print('Exception:', e)
        traceback.print_exc()
        return usatodayrows


def main(weeknum):
    html_content = fetch_usatoday_data(weeknum, 'https://tallysight.com/new/widget/staff-picks/usa-today-sports/nfl/event:2024-25-week-17/default:ml/types:ml,ats/extras:condensed/performances:bboverall,overall?id=5fef16ef-7f0c-41e5-81c9-a000636d9d0c')
    if html_content:
        print(html_content)
    else:
        print("Failed to retrieve data")

if __name__ == "__main__":
    weeknum = sys.argv[0]
    main(weeknum)
