# Python script for web scraping to extract data from a website
import requests, sys, datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv, traceback, array
from scraper_nfl import fetch_nfl_data
from scraper_usatoday import fetch_usatoday_data
from scraper_espn import fetch_espn_data


weeknum = 1

ts = {
    'url': 'https://www.cbssports.com/nfl/news/nfl-week-1-odds-expert-picks-best-bets-teasers-spreads-survivor-picks-tv-streaming-more/',
    'name': 'TerrySullivan',
    'searchTerm': 'Projected score',
    'searchTag': 'strong',
    'endPickTerm': 'The pick:',
    'separator': ', '
    # https://www.cbssports.com/writers/tyler-sullivan/
}
pp = {
    'url': 'https://www.cbssports.com/nfl/news/pete-priscos-week-1-nfl-picks-jaguars-outscore-dolphins-colts-upset-texans-giants-over-vikings/',
    'name': 'PetePrisco',
    'searchTerm': 'Pick:',
    'searchTag': 'strong',
    'separator': ', '
    #https://www.cbssports.com/writers/pete-prisco/
}

breech = {
    'url': 'https://www.cbssports.com/nfl/news/2024-nfl-week-1-picks-dolphins-roll-over-jaguars-jets-upset-49ers-rams-win-thriller-over-lions/',
    'name': 'JohnBreech',
    'searchTerm': 'The pick:',
    'searchTag': 'strong',
    'separator': '-'
    # https://www.cbssports.com/writers/john-breech/
}

foxsports = {
    'url': 'https://www.foxsports.com/articles/nfl/2024-nfl-week-' + str(weeknum) + '-predictions-betting-odds-tv-schedule',
    'name': 'DataSkrive',
    'searchTerm': 'Prediction:',
    'searchTag': 'strong',
    'separator': ', '
}

azc = {
    'url': 'https://www.azcentral.com/story/sports/nfl/2024/09/11/nfl-week-2-predictions-win-probabilities-picks-2024-season/75126241007/',
    'name': 'Jeremy Cluff',
    'searchTerm': 'Prediction:',
    'searchTag': 'strong',
    'separator': ', '
    # https://www.azcentral.com/staff/2648096001/jeremy-cluff/
}

pfn = {
    'url': 'https://www.profootballnetwork.com/week-1-nfl-picks-predictions-2024/',
    'name': 'PFN',
    'searchTerm': 'Prediction:',
    'searchTag': 'strong',
    'separator': ', '
    # https://www.profootballnetwork.com/author/brolfe/
}

sz = {
    'url': 'https://nflspinzone.com/2024-nfl-picks-and-score-predictions-for-week-18-action-01jgchm4ytxr',
    'name': 'NFL Spinzone',
    'searchTerm': 'Prediction:',
    'searchTag': 'strong',
    'separator': ', '
    # https://nflspinzone.com/nfl/
}

cowherd = {
    'url': 'https://foxsportsradio.iheart.com/featured/the-herd-with-colin-cowherd/content/2024-09-06-blazing-five-colin-cowherd-gives-his-5-best-nfl-bets-for-week-1-sep-8/',
    'name': 'ColinCowherd',
    'searchTerm': "prediction:",
    'searchTag': 'em',
    'separator': ', '
}

bleacher = {
    'url': 'https://bleacherreport.com/articles/10134134-bleacher-reports-expert-week-1-nfl-picks',
    'name': 'BleacherReport',
    'searchTerm': 'Score Prediction:',
    'searchTag': 'b',
    'separator': ', '
    # https://bleacherreport.com/nfl
}

bender = {
    'url': 'https://www.sportingnews.com/us/nfl/news/nfl-picks-predictions-week-1-straight-cowboys-chargers/b5dc4eb1ed2f7cec6447f19a',
    'name': 'BillBender',
    'searchTerm': 'Pick:',
    'searchTag': 'strong',
    'separator': ', '
    # https://www.sportingnews.com/us/author/bill-bender
}

iyer = {
    'url': 'https://www.sportingnews.com/us/nfl/news/nfl-picks-predictions-spread-week-1/f80d17b370f1ff4eed5be8ba'
    # https://www.sportingnews.com/us/author/vinnie-iyer
}

thirtythirdteam = {
    'url': 'https://www.the33rdteam.com/2024-nfl-week-' + str(weeknum) + '-expert-picks-predictions-for-every-game/',
    'name': 'MarcusMosher',
    'searchTerm': 'Score Prediction:',
    'searchTag': 'strong',
    'separator': ', '
    # https://www.the33rdteam.com/
}

sportsnaut = {
    'url': 'https://sportsnaut.com/list/nfl-week-' + str(weeknum) + '-predictions/'
    # https://sportsnaut.com/list/nfl-week-6-predictions-2024/
}

usatoday = {
    'url': 'https://tallysight.com/new/widget/staff-picks/usa-today-sports/nfl/event:2024-25-week-1/default:ml/types:ml,ats,ou,props/extras:condensed/performances:bboverall,overall?id=23f825eb-6e7d-46f6-954d-6affff3926c5'
    # https://www.usatoday.com/sports/nfl/
}

espn = {
    'url': 'https://www.espn.com/nfl/story/_/id/41108396/nfl-week-1-picks-schedule-fantasy-football-odds-injuries-stats-2024'
    # https://www.usatoday.com/sports/nfl/
}

writersArray = [ts, pp, bleacher, bender, pfn, sz, foxsports, thirtythirdteam] #, foxsports, azc, 
request_headers = {'User-Agent': 'Mozilla/5.0'}




# article = driver.find_element(By.CLASS_NAME, "Article-content")
# picks = driver.find_element(By.TAG_NAME, "strong")
rows = []
chrome_driver_path = './chromedriver'

service = Service(chrome_driver_path)
weboptions = webdriver.ChromeOptions()
weboptions.add_argument("start-maximized"); # https://stackoverflow.com/a/26283818/1689770
weboptions.add_argument("enable-automation"); # https://stackoverflow.com/a/43840128/1689770
# weboptions.add_argument("--headless"); # only if you are ACTUALLY running headless
weboptions.add_argument("--no-sandbox"); # https://stackoverflow.com/a/50725918/1689770
weboptions.add_argument("--disable-dev-shm-usage"); # https://stackoverflow.com/a/50725918/1689770
weboptions.add_argument("--disable-browser-side-navigation"); # https://stackoverflow.com/a/49123152/1689770
weboptions.add_argument("--disable-gpu"); # https://stackoverflow.com/questions/51959986/how-to-solve-selenium-chromedriver-timed-out-receiving-message-from-renderer-exc

driver = webdriver.Chrome(weboptions)
try:
    for writer in writersArray:
        
        print('writer[\'name\']:', writer['name'])
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

        driver.get(writer['url'])
        wait = WebDriverWait(driver, timeout=2)
        driver.implicitly_wait(10)
        # resultsTable = driver.find_elements_by_xpath("//*[contains(text(), " + writer['searchTerm'] + ")]")
        # wait.until(lambda d : resultsTable.is_displayed())

        picks = driver.find_elements(By.XPATH, "//*[contains(text(), '" + writer['searchTerm'] + "')]/parent::*")
        #find_elements_by_xpath("//*[contains(text(), " + writer['searchTerm'] + ")]")
        # if writer['name'] == 'PetePrisco':
        #     print(response.data)
        # picks = soup.find_all(writer['searchTag'], string = writer['searchTerm']) #, attrs={'class': 'Article-content'}

        # print([t.parent.text for t in soup.findAll('strong', string="Projected score")])
        print('picks length: ', len(picks))
        for p in picks:
            # parent = p.parent.text        
            # colonIndex = parent.find(':')
            pText = p.text
            # print('p:', pText)
            colonIndex = pText.find(':')
            pickIndex = None
            if "endPickTerm" in writer:
                pickIndex = pText.find(writer['endPickTerm'])
            print('195', colonIndex, pickIndex)
            if colonIndex == -1:
                print('pick: ', p)
            if (colonIndex > 0):
                predictionString = ""
                if pickIndex is not None:
                    predictionString = pText[colonIndex+2:pickIndex]
                else:
                    predictionString = pText[colonIndex+2:]
                firstSpace = predictionString.find(" ")
                separator = predictionString.find(writer['separator'])
                secondSpace = predictionString.find(" ", separator+len(writer['separator']))
                winner = predictionString[:firstSpace]
                winnerScore = predictionString[firstSpace:separator]
                loser = predictionString[separator+2:secondSpace]
                loserScore = predictionString[secondSpace:].strip()
                # print([writer['name'],winner, winnerScore, loser, loserScore])
                try:
                    rows.append([writer['name'],winner, int(winnerScore), loser, int(loserScore)])
                except ValueError:
                    print(ValueError, [writer['name'],winner, winnerScore, loser, loserScore])
                # print(winner, int(winnerScore), loser, int(loserScore))

    # # johnbreech formatting

    response = requests.get(breech['url'])
    # print(response)
    soup = BeautifulSoup(response.text, 'html.parser')
    picks = soup.find_all(breech['searchTerm']) #, attrs={'class': 'Article-content'}

    # print([t.parent.text for t in soup.findAll('strong', string="Projected score")])

    for p in picks:
        predictionString = p.text
        separator = predictionString.find("-")
        lastSpace = predictionString.rfind(" ")
        thirdSpace = predictionString.rfind(" ", 0, lastSpace)
        secondSpace = predictionString.rfind(" ", 0, separator)
        firstSpace = predictionString.rfind(" ", 0, secondSpace)
        winner = predictionString[:firstSpace]
        winnerScore = predictionString[firstSpace:separator]
        loser = predictionString[lastSpace:]
        loserScore = predictionString[separator+1:predictionString.find(" over")]
        # print(['Sportsnaut',winner, int(winnerScore), loser, int(loserScore)])
        try:
            rows.append(['JohnBreech',winner, int(winnerScore), loser, int(loserScore)])
        except ValueError:
            print(ValueError)
    # # sportsnaut formatting

    response = requests.get(sportsnaut['url'])
    # print(response)
    soup = BeautifulSoup(response.text, 'html.parser')
    picks = soup.find_all('h2') #, attrs={'class': 'Article-content'}

    # print([t.parent.text for t in soup.findAll('strong', string="Projected score")])

    for p in picks:
        predictionString = p.text
        separator = predictionString.find(", ")
        lastSpace = predictionString.rfind(" ")
        thirdSpace = predictionString.rfind(" ", 0, lastSpace)
        secondSpace = predictionString.rfind(" ", 0, separator)
        firstSpace = predictionString.rfind(" ", 0, secondSpace)
        winner = predictionString[firstSpace+1:secondSpace]
        winnerScore = predictionString[secondSpace:separator]
        loser = predictionString[thirdSpace+1:lastSpace]
        loserScore = predictionString[lastSpace:]
        # print(['Sportsnaut',winner, int(winnerScore), loser, int(loserScore)])
        try:
            rows.append(['Sportsnaut',winner, int(winnerScore), loser, int(loserScore)])
        except ValueError:
            print(ValueError)

    # vinnie iyer formatting
    driver.get(iyer["url"])
    wait = WebDriverWait(driver, timeout=2)
    driver.implicitly_wait(10)
    # resultsTable = driver.find_elements_by_xpath("//*[contains(text(), " + writer['searchTerm'] + ")]")
    # wait.until(lambda d : resultsTable.is_displayed())
    games = driver.find_elements(By.TAG_NAME,"h3")
    picks = driver.find_elements(By.XPATH, "//*[contains(text(), 'Pick:')]/parent::*")
    # response = requests.get()
    # print(response)
    # soup = BeautifulSoup(response.text, 'html.parser')
    # games = soup.find_all('h3')
    # picks = soup.find_all('strong', string="Pick: ") #, attrs={'class': 'Article-content'}

    # print([t.parent.text for t in soup.findAll('strong', string="Projected score")])
    gamesObject = {}
    print('VI games:', len(games))
    for g in games:    
        gameString = g.text
        separatorString = " at "
        separator = gameString.find(separatorString)
        if separator == -1:
            separatorString = " over "
            separator = gameString.find(separatorString)
        oddsIndex = gameString.find("(")
        colonIndex = gameString.find(":")
        addedSpaces = 2
        if colonIndex == -1:
            colonIndex = 0
            addedSpaces = 0
        lastSpace = None
        awayTeam = None
        homeTeam = None
        # print('oddsIndex:', gameString, separator, oddsIndex)
        # "at " appears before the odds; odds are at the end
        if separator < oddsIndex:
            lastSpace = gameString.rfind(" ", 0, oddsIndex)
            homeTeam = gameString[separator+len(separatorString):oddsIndex].strip()
            # print('lastSpace: ', lastSpace, homeTeam)
        else:
            lastSpace = gameString.rfind(" ")
            homeTeam = gameString[lastSpace:].strip()
            # print('lastSpace2: ', lastSpace, homeTeam)
        firstSpace = gameString.find(" ",colonIndex+addedSpaces)
        if (firstSpace == 0):
            firstSpace = gameString.find(" ",1)
        print('firstSpace: ', firstSpace)
        awayTeam = gameString[colonIndex+addedSpaces:firstSpace].strip()
        gamesObject[homeTeam] = {
            "awayTeam": awayTeam,
            "homeTeam": homeTeam
        }
        
        gamesObject[awayTeam] = {
            "awayTeam": awayTeam,
            "homeTeam": homeTeam
        }
    print('VI gamesObject: ', gamesObject)
    print('VI picks:', len(picks))
    for p in picks:
        #Texans win 20-17 and cover the spread.
        predictionString = p.text
        colonIndex = predictionString.find(":")
        scoreSeparatorIndex = predictionString.find("-")
        firstSpace = predictionString.find(" ",colonIndex+2)
        winningTeam = predictionString[colonIndex+2:firstSpace]
        separator = predictionString.find(" win ")
        separatorLength = len(" win ")
        if (separator == -1):
            separator = predictionString.find(" in ")
            separatorLength = len(" in ")
        winnerScore = predictionString[separator+separatorLength:scoreSeparatorIndex]
        lastSpace = predictionString.find(" ",scoreSeparatorIndex)
        loserScore = predictionString[scoreSeparatorIndex+1:lastSpace]
        print('winningTeam, winningScore, losingScore', winningTeam, winnerScore, loserScore)
        
        winner = None
        loser = None
        if winningTeam != "Vinnie":
            if winningTeam in gamesObject:
                if gamesObject[winningTeam]["awayTeam"] == winningTeam:
                    winner = gamesObject[winningTeam]["awayTeam"]
                    loser = gamesObject[winningTeam]["homeTeam"]
                else:
                    winner = gamesObject[winningTeam]["homeTeam"]
                    loser = gamesObject[winningTeam]["awayTeam"]
            else:
                print('winningTeam not found:', winningTeam)
        try: 
            print(['VinnieIyer',winner, int(winnerScore), loser, int(loserScore)])
            rows.append(['VinnieIyer',winner, int(winnerScore), loser, int(loserScore)])
        except ValueError:
            print(ValueError)
            print(['VinnieIyer',winner, winnerScore, loser, loserScore])
            rows.append(['VinnieIyer',winner, winnerScore, loser, loserScore])


    espnrows = fetch_espn_data(weeknum, espn['url'])
    for espnrow in espnrows:
        rows.append(espnrow)

    # dimers formatting
    driver.get('https://www.dimers.com/bet-hub/nfl/schedule')
    driver.implicitly_wait(10)
    matchgrid = driver.find_element(By.CLASS_NAME, "match-list-grid")
    games = matchgrid.find_elements(By.CLASS_NAME,"game-link")    
    firstGame = matchgrid.find_element(By.CLASS_NAME,"game-link")
    
    popup = driver.find_elements(By.CLASS_NAME, "gnt_mol_xb")
    if len(popup) > 0:
        popup[0].click()
    firstGame.click()
    # response = requests.get()
    # print(response)
    # soup = BeautifulSoup(response.text, 'html.parser')
    # games = soup.find_all('h3')
    # picks = soup.find_all('strong', string="Pick: ") #, attrs={'class': 'Article-content'}

    # print([t.parent.text for t in soup.findAll('strong', string="Projected score")])
    
    # print('gamesObject: ', gamesObject)
    g = 0
    while g < len(games)-1: 
        teams = driver.find_elements(By.CLASS_NAME, "team-column")
        if teams is not None and len(teams) > 0:
            wait.until(lambda d : teams[0].is_displayed())
            scores = driver.find_elements(By.CLASS_NAME, "score")
            awayTeam = teams[0].text
            awayScore = scores[0].text
            homeTeam = teams[1].text
            homeScore = scores[1].text
            
            
            print('awayTeam, awayScore, homeTeam, homeScore: ', awayTeam, awayScore, homeTeam, homeScore)
            if awayScore > homeScore:
                winner = awayTeam
                winnerScore = awayScore
                loser = homeTeam
                loserScore = homeScore
            else:
                winner = homeTeam
                winnerScore = homeScore
                loser = awayTeam
                loserScore = awayScore    
                
            rows.append(['Dimers',winner, int(winnerScore), loser, int(loserScore)])
            navButtons = driver.find_elements(By.CLASS_NAME,"match-nav-link")
            navButtons[1].click()
            wait.until(EC.staleness_of(teams[0]))
            g = g + 1
            print('g:', g)
        else:
            g = g + 1

    # usatoday formatting
    
    usatodayrows = fetch_usatoday_data(weeknum, usatoday['url'])
    for usatodayrow in usatodayrows:
        rows.append(usatodayrow)
        
                # /html/body/div[2]/main/article/div[5]/p[10]/a[1] /html/body/div[2]/main/article/div[5]/p[10]/a[1] /html/body/div[2]/main/article/div[5]/p[10]/a[3]

    # nfl formatting
    
    nflrows = fetch_nfl_data(weeknum)
    for nflrow in nflrows:
        rows.append(nflrow)
        
                # /html/body/div[2]/main/article/div[5]/p[10]/a[1] /html/body/div[2]/main/article/div[5]/p[10]/a[1] /html/body/div[2]/main/article/div[5]/p[10]/a[3]


    ### Final Row for printing picks ###
    week1picks = open("2024week" + str(weeknum) + "picks.csv", 'w+', newline='')
    with week1picks as csvfile:
        
        # creating a csv writer object  
        csvwriter = csv.writer(csvfile)  
            
        # writing the fields  
        
        fields = ['Source', 'Winner', 'Winner Score', 'Loser', 'Loser Score']
        csvwriter.writerow(fields)  
            
        # writing the data rows  
        csvwriter.writerows(rows) 
except:    
    print(traceback.print_exc())
    week1picks = open("2024week" + str(weeknum) + "picks.csv", 'w+', newline='')
    with week1picks as csvfile:
        
        # creating a csv writer object  
        csvwriter = csv.writer(csvfile)  
            
        # writing the fields  
        
        fields = ['Source', 'Winner', 'Winner Score', 'Loser', 'Loser Score']
        csvwriter.writerow(fields)  
            
        # writing the data rows  
        csvwriter.writerows(rows) 
# print(picks)
