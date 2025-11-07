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
from scraper_oddsshark import fetch_oddsshark_data
from scraper_dratings import fetch_dratings_data
from scraper_oddstrader import fetch_oddstrader_data
from scraper_nflspinzone import fetch_nflspinzone_data
from scraper_sbr import fetch_sbr_data
from scraper_clutchpoints import fetch_clutchpoints_data



weeknum = int(sys.argv[1])
year = int(sys.argv[2])
season = sys.argv[3]

ts = {
    'url': 'https://www.cbssports.com/nfl/news/nfl-week-10-picks-predictions-road-teams-betting/',
    'name': 'TylerSullivan',
    'searchTerm': 'Projected',
    'searchTag': 'strong',
    'endPickTerm': 'The pick:',
    'separator': ', '
    # https://www.cbssports.com/writers/tyler-sullivan/
}
pp = {
    'url': 'https://www.cbssports.com/nfl/news/priscos-week-10-nfl-picks-buccaneers-slow-down-patriots-packers-edge-eagles/',
    'name': 'PetePrisco',
    'searchTerm': 'Pick:',
    'searchTag': 'strong',
    'separator': ', ',
    'endPickTerm': ' | '
    #https://www.cbssports.com/writers/pete-prisco/
}

breech = {
    'url': 'https://www.cbssports.com/nfl/news/nfl-week-10-picks-score-predictions-vikings-shock-ravens-colts-win-in-germany/',
    'name': 'JohnBreech',
    'searchTerm': 'PICK:',
    'searchTag': 'strong',
    'separator': ' over '
    # https://www.cbssports.com/writers/john-breech/
}

foxsports = {
    'url': 'https://www.foxsports.com/articles/nfl/2025-nfl-week-' + str(weeknum) + '-predictions-betting-odds-tv-schedule',
    'name': 'DataSkrive',
    'searchTerm': 'Prediction:',
    'searchTag': 'strong',
    'separator': ', '
}

azc = {
    'url': 'https://www.azcentral.com/story/sports/nfl/2025/11/03/nfl-week-10-picks-predictions-scores-2025-season/84327978007/',
    'name': 'Jeremy Cluff',
    'searchTerm': 'Prediction:',
    'searchTag': 'strong',
    'separator': ', '
    # https://www.azcentral.com/staff/2648096001/jeremy-cluff/
}

dratings = {
    'url': 'https://www.dratings.com/predictor/nfl-football-predictions/',
    'name': 'DRatings'
}

pfn = {
    'url': 'https://www.profootballnetwork.com/week-' + str(weeknum) + '-nfl-picks-predictions-2025/',
    'name': 'PFN',
    'searchTerm': 'Prediction:',
    'searchTag': 'strong',
    'separator': ', '
    # https://www.profootballnetwork.com/author/brolfe/
}

sz = {
    'url': 'https://nflspinzone.com/2025-nfl-picks-and-score-predictions-for-every-week-10-game-01k95mpa15r7',
    'name': 'NFL Spinzone',
    'searchTerm': 'Prediction:',
    'searchTag': 'strong',
    'separator': ', '
    #   https://www.bing.com/search?FORM=U523DF&PC=U523&q=spinzone+2025+week+10&PC=U316&FORM=CHROMN
}

cowherd = {
    'url': 'https://foxsportsradio.iheart.com/featured/the-herd-with-colin-cowherd/content/2024-09-06-blazing-five-colin-cowherd-gives-his-5-best-nfl-bets-for-week-1-sep-8/',
    'name': 'ColinCowherd',
    'searchTerm': "prediction:",
    'searchTag': 'em',
    'separator': ', '
}

bleacher = {
    'url': 'https://bleacherreport.com/articles/10135758-bleacher-reports-week-3-nfl-picks',
    'name': 'BleacherReport',
    'searchTerm': 'Score Prediction:',
    'searchTag': 'b',
    'separator': ', '
    # https://bleacherreport.com/nfl
}

bender = {
    'url': 'https://www.sportingnews.com/us/nfl/news/nfl-picks-predictions-week-10/8b6c5afbe17f50552b24d376',
    'name': 'BillBender',
    'searchTerm': 'Pick:',
    'searchTag': 'strong',
    'separator': ', '
    # https://www.sportingnews.com/us/author/bill-bender
}

iyer = {
    'url': 'https://www.sportingnews.com/us/nfl/news/nfl-picks-predictions-against-spread-week-10/27985c6c376f3e671262dbb3'
    # https://www.sportingnews.com/us/author/vinnie-iyer
}

thirtythirdteam = {
    "url": 'https://www.the33rdteam.com/2025-nfl-week-' + str(weeknum) + '-expert-picks-predictions-for-every-game/',#'url': 'https://www.the33rdteam.com/2025-nfl-championship-week-expert-picks-predictions-for-every-game/', 
    'name': 'MarcusMosher',
    'searchTerm': 'Score Prediction:',
    'searchTag': 'strong',
    'separator': ', '
    # https://www.the33rdteam.com/
}

sportsnaut = {
    'url': 'https://sportsnaut.com/nfl/nfl-week-' + str(weeknum) + '-predictions-picks-every-game-nfl-schedule-this-week' # https://sportsnaut.com/nfl/nfl-week-8-predictions-picks-every-game-nfl-schedule-this-week 'https://sportsnaut.com/nfl/nfl-analysis/lists/afc-championship-game-predictions-buffalo-bills-vs-kansas-city-chiefs/'
    # https://sportsnaut.com/list/nfl-week-6-predictions-2024/
}

copilot = {
    'url': 'https://www.usatoday.com/story/sports/nfl/2025/11/06/nfl-week-10-picks-predictions-ai/87108339007/', # https://www.usatoday.com/story/sports/nfl/2025/10/16/nfl-week-7-picks-predictions-ai/86697464007/
    'name': 'Copilot',
    'searchXPath': "//h3[@class='gnt_ar_b_h3']", #gnt_ar_b_h3
    'separator': ', '

}

usatoday = {
    'url': 'https://e.infogram.com/d724b98a-d943-462f-a81c-65aeabfdebbe?src=embed#async_embed' #https://e.infogram.com/ad6b49fa-d4a5-4787-b6ae-9e8592ca802a?src=embed#async_embed'
    # https://www.usatoday.com/sports/nfl/
}

espn = {
    'url': 'https://www.espn.com/nfl/story/_/page/viewersguide46858769/nfl-week-10-picks-predictions-schedule-fantasy-football-odds-injuries-stats-2025'
    # https://www.espn.com/nfl/
}

nfl = {
    'url': 'https://www.nfl.com/news/nfl-picks-week-' + str(weeknum) + '-2025-nfl-season'
    # 'https://www.nfl.com/news/week-' + str(weeknum) + '-nfl-picks-2024-nfl-season' - https://www.nfl.com/news/nfl-picks-divisional-round-2024-nfl-season

}

clutchpoints = {
    'url': 'https://clutchpoints.com/nfl/nfl-stories/nfl-picks-predictions-odds-week-' + str(weeknum) + '-2025', #https://clutchpoints.com/nfl/nfl-stories/nfl-picks-predictions-odds-week-3-2025
    'name': 'TimCrean',
    'searchTerm': 'Pick:',
    'searchTag': 'strong',
    'separator': '-'
}

rotowire = {
    'url': 'https://www.rotowire.com/football/article/beating-the-book-nfl-week-10-picks-against-the-spread-score-predictions-98318',
    'name': 'NickWhalen',
    'searchTerm': 'The pick:',
    'separator': ' - '
}

sbr = {
    'url': 'https://www.sportsbookreview.com/picks/nfl/ai-predictions-beat-the-bot-week-' + str(weeknum) + '-2025/'
}

rotoballer = {
    'url': 'https://www.rotoballer.com/nfl-predictions-week-10-picks-and-analysis-for-every-game-2025/1747881',
    'name': 'JimNicely',
    'separator': ', ',
    'searchTag': 'h2',
    'endPickTerm': ' ('
    #https://www.rotoballer.com/author/jnice323
}

# yardbarker = {
#     'url': 'https://www.yardbarker.com/nfl/articles/2024_nfl_week_3_expert_picks_predictions_for_every_game/s1_17304_40918862',
#     'name': 'YardBarker',
#     'searchTerm': 'Score Prediction:',
#     'searchTag': 'strong',
#     'separator': ', '
# }

writersArray = [ts, pp, bender, foxsports, azc, copilot, rotowire, rotoballer] #, sz, foxsports, azc, pfn, 
request_headers = {'User-Agent': 'Mozilla/5.0'}

errors = []





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
weboptions.add_argument("--enable-unsafe-swiftshader")
weboptions.add_argument("--log-level=3")
weboptions.page_load_strategy = 'eager'

driver = webdriver.Chrome(options=weboptions)

driver.set_page_load_timeout(35) # .manage().timeouts().pageLoadTimeout(100, TimeUnit.SECONDS);
try:
    i = 0
    for writer in writersArray:
        print('i: ', i)
        if i % 5 == 0:
            driver.close()
            driver = webdriver.Chrome(options=weboptions)
            driver.set_page_load_timeout(35) # .manage().timeouts().pageLoadTimeout(100, TimeUnit.SECONDS);
        if writer['url'] != '':
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
            print('getting url')
            driver.get(writer['url'])
            print('waiting')
            wait = WebDriverWait(driver, timeout=2)
            driver.implicitly_wait(10)
            print('done waiting')
            # resultsTable = driver.find_elements_by_xpath("//*[contains(text(), " + writer['searchTerm'] + ")]")
            # wait.until(lambda d : resultsTable.is_displayed())
            print('hasattr()', writer.get("searchTerm"))
            searchTerm = writer.get("searchTerm")
            searchTag = writer.get("searchTag")
            searchXPath = writer.get("searchXPath")

            if searchTerm:
                picks = driver.find_elements(By.XPATH, "//*[contains(text(), '" + writer['searchTerm'] + "')]/parent::*")
            elif searchTag:
                picks = driver.find_elements(By.TAG_NAME, writer["searchTag"])
            else:
                picks = driver.find_elements(By.TAG_NAME, writer["searchXPath"])
            #find_elements_by_xpath("//*[contains(text(), " + writer['searchTerm'] + ")]")
            # if writer['name'] == 'PetePrisco':
            #     print(response.data)
            # picks = soup.find_all(writer['searchTag'], string = writer['searchTerm']) #, attrs={'class': 'Article-content'}

            # print([t.parent.text for t in soup.findAll('strong', string="Projected score")])
            print('picks length: ', len(picks))
            if len(picks) == 0:
                print('writer with no picks: ', writer)
            for p in picks:
                # parent = p.parent.text        
                # colonIndex = parent.find(':')
                pText = p.text
                if writer['name'] == "NickWhalen" or writer['name'] == "ChatPilot":
                    print('p:', pText)
                colonIndex = pText.find(':')
                pickIndex = None
                if "endPickTerm" in writer:
                    pickIndex = pText.find(writer['endPickTerm'])
                print('195', colonIndex, pickIndex)
                if colonIndex == -1:
                    print('pick: ', pText)
                if (colonIndex > 0):
                    
                    try:
                        predictionString = ""
                        if pickIndex is not None:
                            predictionString = pText[colonIndex+2:pickIndex]
                        else:
                            predictionString = pText[colonIndex+2:]
                        print('275 predictionString: ', predictionString)
                        firstSpace = predictionString.find(" ")
                        separator = predictionString.find(writer['separator'])
                        secondSpace = predictionString.find(" ", separator+len(writer['separator']))
                        winner = predictionString[:firstSpace]
                        winnerScore = predictionString[firstSpace:separator]
                        loser = predictionString[separator+len(writer['separator']):secondSpace]
                        loserScore = predictionString[secondSpace:].strip()
                        # print([writer['name'],winner, winnerScore, loser, loserScore])
                    
                        rows.append([writer['name'],winner, int(winnerScore), loser, int(loserScore)])
                    except ValueError:
                        errors.append([writer['name'], traceback.print_exc()])
                        print(ValueError, [writer['name'],winner, winnerScore, loser, loserScore])
                    # print(winner, int(winnerScore), loser, int(loserScore))
                else:
                    predictionString = ""
                    
                    try:
                        if pickIndex is not None:
                            predictionString = pText[:pickIndex]
                        else:
                            predictionString = pText
                        print('295 predictionString: ', predictionString)
                        separator = predictionString.find(writer['separator'])
                        
                        spacesNumber = predictionString.rfind(" ", 0, separator)
                        firstSpace = predictionString.find(" ")
                        print('300 spacesNumber, firstSpace: ', separator, spacesNumber, firstSpace)
                        if spacesNumber > firstSpace: # set the first space if there are two spaces before the score
                            firstSpace = spacesNumber
                        print('303 firstSpace: ', firstSpace)
                        secondSpace = predictionString.find(" ", separator+len(writer['separator']))
                        winner = predictionString[:firstSpace]
                        winnerScore = predictionString[firstSpace:separator]
                        spacesNumber = predictionString.rfind(" ")
                        if spacesNumber > secondSpace:
                            secondSpace = spacesNumber
                        print('309 secondspace: ', secondSpace)
                        loser = predictionString[separator+len(writer['separator']):secondSpace]
                        loserScore = predictionString[secondSpace:].strip()
                        # print([writer['name'],winner, winnerScore, loser, loserScore])
                        rows.append([writer['name'],winner, int(winnerScore), loser, int(loserScore)])
                    except ValueError:
                        errors.append([writer['name'], traceback.print_exc()])
                        print(ValueError, [writer['name'],winner, winnerScore, loser, loserScore])
                
        i = i + 1
    # # johnbreech formatting
    try: 
        response = requests.get(breech['url'])
        # print(response)
        soup = BeautifulSoup(response.text, 'html.parser')
        picks = soup.find_all(breech['searchTerm']) #, attrs={'class': 'Article-content'}

        # print([t.parent.text for t in soup.findAll('strong', string="Projected score")])

        for p in picks:
            predictionString = p.text
            separator = predictionString.find("-")
            winnerSpace = predictionString.find(" ")
            overSpace = predictionString.find(" over ")
            secondSpace = predictionString.rfind(" ", 0, separator)
            firstSpace = predictionString.rfind(" ", 0, secondSpace)
            winner = predictionString[:winnerSpace]
            winnerScore = predictionString[firstSpace:separator]
            loser = predictionString[overSpace + len(" over "):]
            loserScore = predictionString[separator+1:predictionString.find(" over")]
            # print(['Sportsnaut',winner, int(winnerScore), loser, int(loserScore)])
            try:
                rows.append(['JohnBreech',winner, int(winnerScore), loser, int(loserScore)])
                driver.close()
            except ValueError:
                errors.append(['JohnBreech', traceback.print_exc()])
                print(ValueError)
                driver.close()
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
                errors.append(['Sportsnaut', traceback.print_exc()])
                print(ValueError)
    except ValueError:
        errors.append(['Breech/Sportsnaut', traceback.print_exc()])
        print('breech ValueError:', ValueError)

    # vinnie iyer formatting
    try: 
        driver.get(iyer["url"])
        # wait = WebDriverWait(driver, timeout=2)
        # driver.implicitly_wait(10)
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
    except ValueError:
        errors.append(['Iyer', traceback.print_exc()])
        print('iyer ValueError: ', ValueError)
        driver.close()


    if espn['url'] is not None:
        espnrows = fetch_espn_data(weeknum, espn['url'], weboptions)
        for espnrow in espnrows:
            rows.append(espnrow)

        # dimers formatting
        try:
            driver.get('https://www.dimers.com/bet-hub/nfl/schedule') # https://www.dimers.com/bet-hub/nfl/schedule
            driver.implicitly_wait(10)
            driver.refresh()
            driver.implicitly_wait(10)

            matchgrid = driver.find_element(By.CLASS_NAME, "match-list-grid")
            games = matchgrid.find_elements(By.CLASS_NAME,"game-link")    
            firstGame = matchgrid.find_element(By.CLASS_NAME,"game-link")
            
            popup = driver.find_elements(By.CLASS_NAME, "gnt_mol_xb")
            if len(popup) > 0:
                wait.until(EC.element_to_be_clickable(popup[0]))
                popup[0].click()
            try: 
                pageBlocker = driver.find_element(By.CLASS_NAME, 'ab-page-blocker')
                if pageBlocker is not None:
                    closeButton = driver.find_element(By.CLASS_NAME, "ab-close-button")
                    wait.until(EC.element_to_be_clickable(closeButton))
                    closeButton.click()
            except:
                print('ad blocker not found')            
            wait.until(EC.element_to_be_clickable(firstGame))
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
                    wait.until(EC.element_to_be_clickable(navButtons[1]))
                    navButtons[1].click()
                    wait.until(EC.staleness_of(teams[0]))
                    g = g + 1
                    print('g:', g)
                else:
                    g = g + 1
        except ValueError:
            print(ValueError)
            print(['dimers',winner, winnerScore, loser, loserScore])
            rows.append(['dimers',winner, winnerScore, loser, loserScore])


    # usatoday formatting
    
    usatodayrows = fetch_usatoday_data(weeknum, usatoday['url'])
    for usatodayrow in usatodayrows:
        rows.append(usatodayrow)
        
                # /html/body/div[2]/main/article/div[5]/p[10]/a[1] /html/body/div[2]/main/article/div[5]/p[10]/a[1] /html/body/div[2]/main/article/div[5]/p[10]/a[3]

    # nfl formatting
    
    nflrows = fetch_nfl_data(weeknum, nfl['url'], weboptions)
    for nflrow in nflrows:
        rows.append(nflrow)
        
                # /html/body/div[2]/main/article/div[5]/p[10]/a[1] /html/body/div[2]/main/article/div[5]/p[10]/a[1] /html/body/div[2]/main/article/div[5]/p[10]/a[3]

    oddssharkrows = fetch_oddsshark_data(weeknum, weboptions)
    for oddssharkrow in oddssharkrows:
        rows.append(oddssharkrow)
        
    dratingsrows = fetch_dratings_data(weeknum, weboptions)
    for dratingsrow in dratingsrows:
        rows.append(dratingsrow)

    oddstraderrows = fetch_oddstrader_data(weeknum, weboptions)
    for oddstraderrow in oddstraderrows:
        rows.append(oddstraderrow)

        

    nflspinzonerows = fetch_nflspinzone_data(sz['url'], weeknum, weboptions)
    for nflspinzonerow in nflspinzonerows:
        rows.append(nflspinzonerow)

    sbrrows = fetch_sbr_data(weeknum, sbr['url'], weboptions)
    for sbrrow in sbrrows:
        rows.append(sbrrow)

    clutchpointsrows = fetch_clutchpoints_data(weeknum, clutchpoints['url'], weboptions)
    for clutchpointsrow in clutchpointsrows:
        rows.append(clutchpointsrow)

    ### Final Row for printing picks ###
    week1picks = open(str(year) + season + "week" + str(weeknum) + "picks.csv", 'w+', newline='')
    with week1picks as csvfile:
        
        # creating a csv writer object  
        csvwriter = csv.writer(csvfile)  
            
        # writing the fields  
        
        fields = ['Source', 'Winner', 'Winner Score', 'Loser', 'Loser Score']
        csvwriter.writerow(fields)  
            
        # writing the data rows  
        csvwriter.writerows(rows) 
        csvwriter.writerows(errors)
except:    
    print(traceback.print_exc())
    week1picks = open(str(year) + season + "week" + str(weeknum) + "picks.csv", 'w+', newline='')
    with week1picks as csvfile:
        
        # creating a csv writer object  
        csvwriter = csv.writer(csvfile)  
            
        # writing the fields  
        
        fields = ['Source', 'Winner', 'Winner Score', 'Loser', 'Loser Score']
        csvwriter.writerow(fields)  
            
        # writing the data rows  
        csvwriter.writerows(rows) 
        csvwriter.writerows(errors)
# print(picks)
