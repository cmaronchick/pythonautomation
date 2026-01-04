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
weboptionsHC = webdriver.ChromeOptions()
weboptionsHC.accept_insecure_certs = True
weboptionsHC.add_argument('--ignore-certificate-errors')
weboptionsHC.add_argument('disable-notifications')
weboptionsHC.add_argument("--log-level=3")
weboptionsHC.page_load_strategy = 'eager'
articleNumber = 16
def fetch_clutchpoints_data(weeknum, url, weboptions):
    
    clutchpoints = {
        'name': 'TimCrean',
        'searchTerm': 'Pick:',
        'searchTag': 'strong',
        'separator': ', '
        #   https://clutchpoints.com/author/sayrebedinger/
    }
    driver = webdriver.Chrome(options=weboptions)
    driver.set_page_load_timeout(35)
    print('fetch_clutchpoints_data:', url)
    clutchpointsrows = []
    try:
        i = 0
        driver.get(url)
        
        wait = WebDriverWait(driver, timeout=10)
        
        
        # response = requests.get(writer['url'], headers=request_headers)
        # response = requests.get(writer['url'])
        # print(response)
        # soup = BeautifulSoup(response.text, 'html.parser')
        # picks = soup.find_all('strong', string = writer['searchTerm']) #, attrs={'class': 'Article-content'}

        # http = urllib3.PoolManager()
        # response = http.request('GET', writer['url'], headers=request_headers)
        # print(response.status)
        # soup = BeautifulSoup(response.data, 'html.parser')
        
        # weboptions.add_argument("silentDriverLogs=true")
        # weboptions.set_capability("accept")
        # weboptions.add_argument('--ignore-certificate-errors')
        # weboptions.add_argument('--ignore-ssl-errors')


        # resultsTable = driver.find_elements_by_xpath("//*[contains(text(), " + writer['searchTerm'] + ")]")
        
        print('hasattr()', clutchpoints.get("searchTerm"))
        article = driver.find_element(By.TAG_NAME, "article")
        wait.until(lambda d : article.is_displayed())
        searchTerm = clutchpoints.get("searchTerm")
        if searchTerm:
            picks = article.find_elements(By.XPATH, "//strong[contains(text(), '" + clutchpoints['searchTerm'] + "')]/parent::*")
        else:
            picks = article.find_elements(By.XPATH, clutchpoints["searchTag"])
        #find_elements_by_xpath("//*[contains(text(), " + writer['searchTerm'] + ")]")
        # if writer['name'] == 'PetePrisco':
        #     print(response.data)
        # picks = soup.find_all(writer['searchTag'], string = writer['searchTerm']) #, attrs={'class': 'Article-content'}

        # print([t.parent.text for t in soup.findAll('strong', string="Projected score")])
        print('picks length: ', len(picks))
        if len(picks) == 0:
            print('writer with no picks: ', clutchpoints)
        # teamPairings = driver.find_elements(By.XPATH, "//h3[contains(text(), '@')]")
        # teamsArray = []
        # # for pairing in teamPairings:
        # for pairing in teamPairings:
        #     try: 
        #         teams = pairing.text.split(' @ ')
        #         t = 0
        #         teamObject = {}
        #         for team in teams:
        #             if t == 0:
        #                 teamObject["awayTeam"] = team
        #             elif t == 1:
        #                 teamObject["homeTeam"] = team[:team.find(",")]
        #             t = t + 1
        #             teamsArray.append(teamObject)
        #     except Exception as e:                    
        #         print('Exception:', e)
        #         traceback.print_exc()
        # print('teamsArray: ', teamsArray)
        # pInt = 0
        # 275 predictionString:  Lions 30-27 over Chiefs | Lions +1.5 | Odds via DraftKings, where new users get $200 in bonus bets with a wining $5 wager. Click here to get started:
        # # <class 'ValueError'> ['JohnBreech', 'Lions', ' 30', '27', 'over Chiefs | Lions +1.5 | Odds via DraftKings, where new users get $200 in bonus bets with a wining $5 wager. Click here to get started:']
        pickNum = 0
        for p in picks:
            
            # driver.refresh()
            # article = driver.find_element(By.TAG_NAME, "article")
            # picks = article.find_elements(By.XPATH, "//" + clutchpoints['searchTag'] + "[contains(text(), '" + clutchpoints['searchTerm'] + "')]/parent::*")
            # p = picks[pickNum]
            try: 
                winner = ''
                loser = ''
                # parent = p.parent.text        
                # colonIndex = parent.find(':')
                pText = p.text
                print('p:', pText)
                predictionString = ""
                predictionString = pText
                # print('predictionString: ', predictionString)
                colonIndex = predictionString.find(":")+1
                firstSpace = predictionString.find(" ", colonIndex+1)
                dashIndex = predictionString.find("-")
                winner = predictionString[colonIndex+1:firstSpace]
                winnerScore = predictionString[firstSpace + 1:dashIndex]
                loserScore = predictionString[dashIndex+1:].strip()
                # print([clutchpoints['name'],winner, winnerScore, loser, loserScore])
                try:
                    clutchpointsrows.append(['clutchpoints',winner, int(winnerScore), loser, int(loserScore)])
                    # clutchpointsrows.append(['oddsshark', awayTeam, awayTeamScore, homeTeam, homeTeamScore])
                except ValueError:
                    print(ValueError, [clutchpoints['name'],winner, winnerScore, loser, loserScore])
                # pInt = pInt + 1
            except Exception as e:
                print('Exception:', e)
                # traceback.print_exc()
            pickNum = pickNum + 1
        # print('clutchpointsrows:', clutchpointsrows)
        driver.quit()
        return clutchpointsrows
    except Exception as e:
        print('Exception:', e)
        traceback.print_exc()
        driver.quit()
        return clutchpointsrows


def main(weeknum, weboptions):
    if weeknum == None:
        weeknum = sys.argv[1]
    url = "https://clutchpoints.com/nfl/nfl-stories/nfl-picks-predictions-odds-week-7-2025"
    html_content = fetch_clutchpoints_data(weeknum, url, weboptions) #'https://tallysight.com/new/widget/staff-picks/usa-today-sports/nfl/event:2024-25-week-17/default:ml/types:ml,ats/extras:condensed/performances:bboverall,overall?id=5fef16ef-7f0c-41e5-81c9-a000636d9d0c'
    if html_content:
        print(html_content)
    else:
        print("Failed to retrieve data")

if __name__ == "__main__":
    weeknum = sys.argv[0]
    main(weeknum, weboptionsHC)
