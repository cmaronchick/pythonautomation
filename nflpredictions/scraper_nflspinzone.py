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
    "https://nflspinzone.com/2025-nfl-picks-score-predictions-for-every-week-2-game-01k4mymqtnxj",
    "https://nflspinzone.com/2025-nfl-picks-score-predictions-for-every-week-2-game-01k4mymqtnxj/2",
    "https://nflspinzone.com/2025-nfl-picks-score-predictions-for-every-week-2-game-01k4mymqtnxj/3",
    "https://nflspinzone.com/2025-nfl-picks-score-predictions-for-every-week-2-game-01k4mymqtnxj/4",
    "https://nflspinzone.com/2025-nfl-picks-score-predictions-for-every-week-2-game-01k4mymqtnxj/5",
    "https://nflspinzone.com/2025-nfl-picks-score-predictions-for-every-week-2-game-01k4mymqtnxj/6",
    "https://nflspinzone.com/2025-nfl-picks-score-predictions-for-every-week-2-game-01k4mymqtnxj/7",
    "https://nflspinzone.com/2025-nfl-picks-score-predictions-for-every-week-2-game-01k4mymqtnxj/8",
    "https://nflspinzone.com/2025-nfl-picks-score-predictions-for-every-week-2-game-01k4mymqtnxj/9",
    "https://nflspinzone.com/2025-nfl-picks-score-predictions-for-every-week-2-game-01k4mymqtnxj/10",
    "https://nflspinzone.com/2025-nfl-picks-score-predictions-for-every-week-2-game-01k4mymqtnxj/11",
    "https://nflspinzone.com/2025-nfl-picks-score-predictions-for-every-week-2-game-01k4mymqtnxj/12",
    "https://nflspinzone.com/2025-nfl-picks-score-predictions-for-every-week-2-game-01k4mymqtnxj/13",
    "https://nflspinzone.com/2025-nfl-picks-score-predictions-for-every-week-2-game-01k4mymqtnxj/14",
    "https://nflspinzone.com/2025-nfl-picks-score-predictions-for-every-week-2-game-01k4mymqtnxj/15",
    "https://nflspinzone.com/2025-nfl-picks-score-predictions-for-every-week-2-game-01k4mymqtnxj/16"
    
]


sz = {
    'url': 'https://nflspinzone.com/2025-nfl-picks-score-predictions-for-every-week-3-game',
    'name': 'NFL Spinzone',
    'searchTerm': 'win ',
    'searchTag': 'em',
    'separator': '-'
    #   https://nflspinzone.com/posts/2024-nfl-picks-score-predictions-for-week-3-01j7xet93n9e
}

chrome_driver_path = './chromedriver'

service = Service(chrome_driver_path)
weboptionsHC = webdriver.ChromeOptions()
weboptionsHC.accept_insecure_certs = True
weboptionsHC.add_argument('--ignore-certificate-errors')
weboptionsHC.add_argument('disable-notifications')
weboptionsHC.add_argument("--log-level=3")
weboptionsHC.page_load_strategy = 'eager'
articleNumber = 16
def fetch_nflspinzone_data(url, weeknum, weboptions):
    
    sz = {
         # https://nflspinzone.com/2025-nfl-picks-and-score-predictions-for-every-week-8-game
        'name': 'NFL Spinzone',
        'searchTerm': 'Prediction:',
        'searchTag': 'strong',
        'separator': ', '
        #   https://nflspinzone.com/author/sayrebedinger/
    }
    driver = webdriver.Chrome(options=weboptions)
    print('fetch_nflspinzone_data:')
    nflspinzonerows = []
    try:
        i = 0
        driver.get(url)
        
        wait = WebDriverWait(driver, timeout=2)
        driver.implicitly_wait(5)
        buttonIsClickable = True
        while buttonIsClickable:
        
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
            
            print('hasattr()', sz.get("searchTerm"))
            searchTerm = sz.get("searchTerm")
            if searchTerm:
                picks = driver.find_elements(By.XPATH, "//*[contains(text(), '" + sz['searchTerm'] + "')]/parent::*")
            else:
                picks = driver.find_elements(By.XPATH, sz["searchTag"])
            #find_elements_by_xpath("//*[contains(text(), " + writer['searchTerm'] + ")]")
            # if writer['name'] == 'PetePrisco':
            #     print(response.data)
            # picks = soup.find_all(writer['searchTag'], string = writer['searchTerm']) #, attrs={'class': 'Article-content'}

            # print([t.parent.text for t in soup.findAll('strong', string="Projected score")])
            print('picks length: ', len(picks))
            if len(picks) == 0:
                print('writer with no picks: ', url)
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
            for p in picks:
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
                    winIndex = predictionString.find(" win ")
                    dashIndex = predictionString.find("-")
                    winner = predictionString[:winIndex]
                    winnerScore = predictionString[winIndex + len(" win "):dashIndex]
                    loserScore = predictionString[dashIndex+1:].strip()
                    # print([sz['name'],winner, winnerScore, loser, loserScore])
                    try:
                        nflspinzonerows.append(['NFLSpinzone',winner, int(winnerScore), loser, int(loserScore)])
                        # nflspinzonerows.append(['oddsshark', awayTeam, awayTeamScore, homeTeam, homeTeamScore])
                    except ValueError:
                        print(ValueError, [sz['name']])
                    # pInt = pInt + 1 ,winner, winnerScore, loser, loserScore
                except Exception as e:
                    print('Exception:', e)
                    traceback.print_exc()
            nextButton = driver.find_element(By.ID, "next-button")
            wait.until(lambda d : nextButton.is_displayed())
            wait.until(EC.element_to_be_clickable(nextButton))
            print('nextButton.get_attribute(\'disabled\'):', nextButton.get_attribute('disabled'))
            if nextButton.get_attribute('disabled') is not None:
                buttonIsClickable = False
            else:
                nextButton.click()
            i = i + 1
        print('nflspinzonerows:', nflspinzonerows)
        driver.close()
        return nflspinzonerows
    except Exception as e:
        print('Exception:', e)
        traceback.print_exc()
        driver.close()
        return nflspinzonerows


def main(weeknum, weboptions):
    html_content = fetch_nflspinzone_data(weeknum, weboptions) #'https://tallysight.com/new/widget/staff-picks/usa-today-sports/nfl/event:2024-25-week-17/default:ml/types:ml,ats/extras:condensed/performances:bboverall,overall?id=5fef16ef-7f0c-41e5-81c9-a000636d9d0c'
    if html_content:
        print(html_content)
    else:
        print("Failed to retrieve data")

if __name__ == "__main__":
    weeknum = sys.argv[0]
    main(weeknum, weboptionsHC)
