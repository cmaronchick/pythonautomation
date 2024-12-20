# Python script for web scraping to extract data from a website
import sys, re, traceback
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
weboptions.add_argument('--ignore-certificate-errors')
weboptions.add_argument('disable-notifications')
driver = webdriver.Chrome(options=weboptions)
def fetch_usatoday_data(weeknum, url):
    print('fetch_usatoday_data:', url)
    usatodayrows = []
    # usatoday formatting
        
    driver.get(url)
    wait = WebDriverWait(driver, timeout=2)
    driver.implicitly_wait(3)
    
    original_window = driver.current_window_handle
    windowhandles = len(driver.window_handles)
    # resultsTable = driver.find_elements_by_xpath("//*[contains(text(), " + writer['searchTerm'] + ")]")
    
    articleBody = driver.find_element(By.TAG_NAME, "article")
    pickLinkIndex = 0
    wait.until(lambda d : articleBody.is_displayed())
    pickLinks = articleBody.find_elements(By.XPATH,'//a[contains(text(), " vs. ")]')    # pickLinks2 = driver.find_elements(By.XPATH, "/html/body/div[3]/main/article/div[5]/p[10]/a")
    print('usatoday picklinks 37:', len(pickLinks))
    while pickLinkIndex < len(pickLinks):
        
        popup = driver.find_elements(By.CLASS_NAME, "gnt_mol_xb")
        if len(popup) > 0:
            popup[0].click()
        pickLinks[pickLinkIndex].click()
        if len(driver.window_handles) > 1:
            driver.switch_to.window(driver.window_handles[len(driver.window_handles)-1])
        articleBody = driver.find_element(By.TAG_NAME, "article")
        wait.until(lambda d : articleBody.is_displayed())
        title = driver.find_element(By.TAG_NAME, "h1")
        wait.until(lambda d : title.is_displayed())
        headers = driver.find_elements(By.TAG_NAME, "h2")
        headerIndex = 0
        for header in headers:
            winnerScore = None
            winningTeam = None
            losingScore = None
            losingTeam = None
            if headerIndex > 1:
                separatorIndex = header.text.find(":")
                author = header.text[:separatorIndex].replace(" ","")
                winner = header.text[separatorIndex+2:header.text.find(",")].split(" ")
                winningTeam = winner[0]
                if len(winner) > 1:
                    winningScore = winner[1]
                loser = header.text[header.text.find(",")+2:].split(" ")
                losingTeam = loser[0]
                if len(loser) > 1:
                    losingScore = loser[1]
                print('author:', author, winningTeam, winningScore, losingTeam, losingScore)
                usatodayrows.append([author,winningTeam, winningScore, losingTeam, losingScore])                    
            headerIndex = headerIndex + 1
        pickLinkIndex = pickLinkIndex + 1 
        driver.get(url)
        popup = driver.find_elements(By.CLASS_NAME, "gnt_mol_xb")
        if len(popup) > 0:
            popup[0].click()
        articleBody = driver.find_element(By.TAG_NAME, "article")
        wait.until(lambda d : articleBody.is_displayed())

        pickLinks = articleBody.find_elements(By.XPATH,'//a[contains(text(), " vs. ")]')
        print('usatoday picklinks 80:', len(pickLinks))
    print('usatodayrows:', usatodayrows)
    return usatodayrows


def main(weeknum):
    html_content = fetch_usatoday_data(weeknum, 'https://www.usatoday.com/story/sports/nfl/2024/12/18/broncos-chargers-game-predictions-picks-odds-week-16/76950456007/')
    if html_content:
        print(html_content)
    else:
        print("Failed to retrieve data")

if __name__ == "__main__":
    weeknum = sys.argv[0]
    main(weeknum)
