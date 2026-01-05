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
def fetch_copilot_data(weeknum, url, weboptions):
    
    copilot = {
        'name': 'Copilot',
        'searchXPath': "//h3[@class='gnt_ar_b_h3']", #gnt_ar_b_h3
        'separator': ', '
    }
    driver = webdriver.Chrome(options=weboptions)
    driver.set_page_load_timeout(20)
    print('fetch_copilot_data:', url)
    copilotrows = []
    try:
        i = 0
        driver.get(url)
        
        wait = WebDriverWait(driver, timeout=5)
        
        
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
        
        print('hasattr()', copilot.get("searchTerm"))
        article = wait.until(EC.presence_of_element_located((By.TAG_NAME, "article")))
        searchTerm = copilot.get("searchTerm")
        if searchTerm:
            picks = article.find_elements(By.XPATH, "//strong[contains(text(), '" + copilot['searchTerm'] + "')]/parent::*")
        else:
            picks = article.find_elements(By.XPATH, copilot["searchXPath"])
        #find_elements_by_xpath("//*[contains(text(), " + writer['searchTerm'] + ")]")
        # if writer['name'] == 'PetePrisco':
        #     print(response.data)
        # picks = soup.find_all(writer['searchTag'], string = writer['searchTerm']) #, attrs={'class': 'Article-content'}

        # print([t.parent.text for t in soup.findAll('strong', string="Projected score")])
        print('picks length: ', len(picks))
        if len(picks) == 0:
            print('writer with no picks: ', copilot)
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
            # picks = article.find_elements(By.XPATH, "//" + copilot['searchTag'] + "[contains(text(), '" + copilot['searchTerm'] + "')]/parent::*")
            # p = picks[pickNum]
            try: 
                winner = ''
                loser = ''
                # parent = p.parent.text        
                # colonIndex = parent.find(':')
                pText = p.text
                # print('p:', pText)
                predictionString = ""
                predictionString = pText
                # print('predictionString: ', predictionString)
                teams = predictionString.split(",")
                winningTeam = teams[0]
                losingTeam = teams[1]
                firstSpace = winningTeam.rfind(" ")
                secondSpace = losingTeam.rfind(" ")
                # print('firtSpace, secondSpace: ', firstSpace, secondSpace)
                winner = predictionString[:firstSpace]
                winnerScore = winningTeam[firstSpace + 1:]
                loser = losingTeam[:secondSpace]
                loserScore = losingTeam[secondSpace+1:]
                # print([copilot['name'],winner, winnerScore, loser, loserScore])
                try:
                    copilotrows.append(['copilot',winner, int(winnerScore), loser, int(loserScore)])
                    # copilotrows.append(['oddsshark', awayTeam, awayTeamScore, homeTeam, homeTeamScore])
                except ValueError:
                    print(ValueError, [copilot['name'],winner, winnerScore, loser, loserScore])
                # pInt = pInt + 1
            except Exception as e:
                print('Exception:', e)
                # traceback.print_exc()
            pickNum = pickNum + 1
        # print('copilotrows:', copilotrows)
        driver.quit()
        return copilotrows
    except Exception as e:
        print('Exception:', e)
        traceback.print_exc()
        driver.quit()
        return copilotrows


def main(weeknum, weboptions):
    if weeknum == None:
        weeknum = sys.argv[1]
    url = "https://www.usatoday.com/story/sports/nfl/2025/11/20/nfl-week-12-picks-predictions-ai/87342519007/" # 'url': 'https://www.usatoday.com/story/sports/nfl/2025/11/20/nfl-week-12-picks-predictions-ai/87342519007/', # https://www.usatoday.com/story/sports/nfl/2025/10/16/nfl-week-7-picks-predictions-ai/86697464007/
    html_content = fetch_copilot_data(weeknum, url, weboptions) #'https://tallysight.com/new/widget/staff-picks/usa-today-sports/nfl/event:2024-25-week-17/default:ml/types:ml,ats/extras:condensed/performances:bboverall,overall?id=5fef16ef-7f0c-41e5-81c9-a000636d9d0c'
    if html_content:
        print(html_content)
    else:
        print("Failed to retrieve data")

if __name__ == "__main__":
    weeknum = sys.argv[0]
    main(weeknum, weboptionsHC)
