# Python script for web scraping to extract data from a website
import sys, re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Setup the Chrome WebDriver

chrome_driver_path = './chromedriver'

service = Service(chrome_driver_path)
weboptions = webdriver.ChromeOptions()
weboptions.accept_insecure_certs = True
driver = webdriver.Chrome(options=weboptions)
def fetch_usatoday_data(weeknum):
    usatodayrows = []
    try:
        driver.get('https://tallysight.com/new/widget/staff-picks/usa-today-sports/nfl/event:2024-25-week-15/default:ml/types:ml,ats/extras:condensed/performances:bboverall,overall')
        wait = WebDriverWait(driver, timeout=2)
        # driver.implicitly_wait(10)
        # resultsTable = driver.find_elements_by_xpath("//*[contains(text(), " + writer['searchTerm'] + ")]")
        table = driver.find_element(By.TAG_NAME, "table")
        wait.until(lambda d : table.is_displayed())
        writers = table.find_elements(By.TAG_NAME, "th")
        print(len(writers))
        writersText = []
        writerIndex = 0
        for writer in writers:
            if writerIndex > 0:
                writersText.append({ "name": re.sub(r'\s+', '', writer.text), "prediction": "", "index": writerIndex})
            writerIndex = writerIndex + 1
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
        print(usatodayrows)
        return usatodayrows
            

    except Exception as e:
        # Close the browser
        print('usatoday exception: ', e)
        return usatodayrows


def main(weeknum):
    html_content = fetch_usatoday_data(weeknum)
    if html_content:
        print(html_content)
    else:
        print("Failed to retrieve data")

if __name__ == "__main__":
    weeknum = sys.argv[0]
    main(weeknum)
