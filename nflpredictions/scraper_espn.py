import requests, sys, datetime, csv
from bs4 import BeautifulSoup
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
weboptions.add_argument("--log-level=3")

# espn formatting
def fetch_espn_data(weeknum, url, weboptions):
    driver = webdriver.Chrome(options=weboptions)
    espnrows = []
    try: 
        driver.get(url)
        wait = WebDriverWait(driver, timeout=2)
        driver.implicitly_wait(10)
        # resultsTable = driver.find_elements_by_xpath("//*[contains(text(), " + writer['searchTerm'] + ")]")
        # wait.until(lambda d : resultsTable.is_displayed())
        gamesBody = driver.find_element(By.CLASS_NAME, "article-body")
        picksGraph = gamesBody.find_elements(By.XPATH, "//*[contains(text(), 'pick:')]/parent::*")  
        # response = requests.get()
        # print(response)
        # soup = BeautifulSoup(response.text, 'html.parser')
        # games = soup.find_all('h3')
        # picks = soup.find_all('strong', string="Pick: ") #, attrs={'class': 'Article-content'}

        # print([t.parent.text for t in soup.findAll('strong', string="Projected score")])
        print('ESPN picks:', len(picksGraph))
        picks = []
        for graphs in picksGraph:
            splitPicks = graphs.text.split("\n")
            print('splitPicks:', splitPicks)
            for pick in splitPicks:
                picks.append(pick)
        print('picks:', len(picks), picks)
        for pick in picks:
            predictionString = pick
            print('predictionString: ', predictionString)
            if predictionString.find("FPI") > -1:
                continue
            separatorString = ", "
            separator = predictionString.find(separatorString)
            if separator == -1:
                separatorString = " over "
                separator = predictionString.find(separatorString)
            separatorLength = len(separatorString)
            colonIndex = predictionString.find(":")
            addedSpaces = 2
            if colonIndex == -1:
                colonIndex = 0
                addedSpaces = 0
            lastSpace = None
            winningTeam = None
            losingTeam = None
            apostrophe = predictionString.find("'s")
            writer = predictionString[:apostrophe]
            print('writer:', writer)
            firstSpace = predictionString.find(" ",colonIndex+2)
            print('firstSpace: ', firstSpace)
            winningTeam = predictionString[colonIndex+2:firstSpace].strip()
            winnerScore = predictionString[firstSpace+1:separator]
            lastSpace = predictionString.rfind(" ")
            losingTeam = predictionString[separator+separatorLength:lastSpace].strip()
            loserScore = predictionString[lastSpace+1:].strip()
            print('winningTeam, winningScore, losingScore', winningTeam, winnerScore, losingTeam, loserScore)
            
            print([writer + 'ESPN',winningTeam, winnerScore, losingTeam, loserScore])
            espnrows.append([writer + 'ESPN',winningTeam, winnerScore, losingTeam, loserScore])
        return espnrows
    except Exception as e:
        print('espn exception: ', e)
        return espnrows
def main(weeknum, weboptions):
    print('weeknum:', weeknum)
    html_content = fetch_espn_data(weeknum,'https://www.espn.com/nfl/story/_/page/viewersguide46941264/nfl-week-11-picks-predictions-schedule-fantasy-football-odds-injuries-stats-2025', {})
    if html_content:
        print(html_content)
        return html_content
    else:
        print("Failed to retrieve data")

if __name__ == "__main__":
    espnrows = main(sys.argv[1], {})
    print('espnrows:', espnrows)

    week1picks = open("2024week" + str(sys.argv[1]) + "espnpicks.csv", 'w+', newline='')
    with week1picks as csvfile:
        
        # creating a csv writer object  
        csvwriter = csv.writer(csvfile)  
            
        # writing the fields  
        
        fields = ['Source', 'Winner', 'Winner Score', 'Loser', 'Loser Score']
        csvwriter.writerow(fields)  
            
        # writing the data rows  
        csvwriter.writerows(espnrows) 