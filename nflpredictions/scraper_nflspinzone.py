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
    'url': 'https://nflspinzone.com/2025-nfl-picks-score-predictions-for-every-week-2-game-01k4mymqtnxj',
    'name': 'NFL Spinzone',
    'searchTerm': 'Prediction:',
    'searchTag': 'strong',
    'separator': '-'
    #   https://nflspinzone.com/posts/2024-nfl-picks-score-predictions-for-week-3-01j7xet93n9e
}

chrome_driver_path = './chromedriver'

service = Service(chrome_driver_path)
# weboptions = webdriver.ChromeOptions()
# weboptions.accept_insecure_certs = True
# weboptions.add_argument('--ignore-certificate-errors')
# weboptions.add_argument('disable-notifications')
# weboptions.add_argument("--log-level=3")
# weboptions.page_load_strategy = 'eager'
articleNumber = 16
def fetch_nflspinzone_data(weeknum, weboptions):
    driver = webdriver.Chrome(options=weboptions)
    print('fetch_oddstrader_data:')
    nflspinzonerows = []
    try:
        i = 0
        driver.get(sz.get('url'))
        
        wait = WebDriverWait(driver, timeout=2)
        while i < articleNumber:
        
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
            # wait.until(lambda d : resultsTable.is_displayed())
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
                print('writer with no picks: ', sz)
            for p in picks:
                winner = ''
                loser = ''
                # parent = p.parent.text        
                # colonIndex = parent.find(':')
                pText = p.text
                # print('p:', pText)
                colonIndex = pText.find(':')
                pickIndex = None
                print('195', colonIndex, pickIndex)
                if colonIndex == -1:
                    print('pick: ', pText)
                if (colonIndex > 0):
                    predictionString = ""
                    if pickIndex is not None:
                        predictionString = pText[colonIndex+2:pickIndex]
                    else:
                        predictionString = pText[colonIndex+2:]
                    print('predictionString: ', predictionString)
                    firstSpace = predictionString.find(" ")
                    separator = predictionString.find(sz['separator'])
                    secondSpace = predictionString.rfind(" ", separator+len(sz['separator']))
                    winner = predictionString[:firstSpace]
                    winnerScore = predictionString[secondSpace:separator]
                    loserScore = predictionString[separator:].strip()
                    # print([sz['name'],winner, winnerScore, loser, loserScore])
                    try:
                        nflspinzonerows.append([sz['name'],winner, int(winnerScore), loser, int(loserScore)])
                    except ValueError:
                        print(ValueError, [sz['name'],winner, winnerScore, loser, loserScore])
                    # print(winner, int(winnerScore), loser, int(loserScore))
                    i = i + 1
                else:
                    predictionString = ""
                    if pickIndex is not None:
                        predictionString = pText[colonIndex+2:pickIndex]
                    else:
                        predictionString = pText[colonIndex+2:]
                    print('predictionString: ', predictionString)
                    spacesNumber = predictionString.rfind(" ", predictionString.find(sz['separator']))
                    firstSpace = predictionString.find(" ")
                    if spacesNumber > firstSpace: # set the first space if there are two spaces before the score
                        firstSpace = spacesNumber
                    separator = predictionString.find(sz['separator'])
                    # secondSpace = predictionString.rfind(" ", separator+len(sz['separator']))
                    # spacesNumber = predictionString.rfind(" ")
                    # if spacesNumber > secondSpace:
                    #     secondSpace = spacesNumber
                    secondSpace = predictionString.rfind(" ", separator+len(sz['separator']))
                    winner = predictionString[:firstSpace]
                    winnerScore = predictionString[secondSpace:separator]
                    loserScore = predictionString[separator:].strip()
                    # print([sz['name'],winner, winnerScore, loser, loserScore])
                    try:
                        nflspinzonerows.append([sz['name'],winner, int(winnerScore), loser, int(loserScore)])
                    except ValueError:
                        print(ValueError, [sz['name'],winner, winnerScore, loser, loserScore])
            driver.find_element(By.ID, "next-button-bottom").click()
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
    main(weeknum)
