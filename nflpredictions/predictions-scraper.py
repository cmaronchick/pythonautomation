# Python script for web scraping to extract data from a website
import requests, sys, datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException, StaleElementReferenceException
import csv, traceback, array
import threading
from contextlib import contextmanager
from scraper_nfl import fetch_nfl_data
from scraper_usatoday import fetch_usatoday_data
from scraper_espn import fetch_espn_data
from scraper_oddsshark import fetch_oddsshark_data
from scraper_dratings import fetch_dratings_data
from scraper_oddstrader import fetch_oddstrader_data
from scraper_nflspinzone import fetch_nflspinzone_data
from scraper_sbr import fetch_sbr_data
from scraper_clutchpoints import fetch_clutchpoints_data
from scraper_copilot import fetch_copilot_data
from scraper_rotowire import fetch_rotowire_data

weeknum = int(sys.argv[1])
year = int(sys.argv[2])
season = sys.argv[3]

ts = {
    'url': 'https://www.cbssports.com/nfl/news/nfl-week-18-picks-best-bets-predictions/',
    'name': 'TylerSullivan',
    'searchTerm': 'Projected',
    'searchTag': 'strong',
    'endPickTerm': 'The pick:',
    'separator': ', '
    # https://www.cbssports.com/writers/tyler-sullivan/
}
pp = {
    'url': 'https://www.cbssports.com/nfl/news/priscos-week-18-nfl-picks-best-bets-predictions/',
    'name': 'PetePrisco',
    'searchTerm': 'Pick:',
    'searchTag': 'strong',
    'separator': ', ',
    'endPickTerm': ' | '
    #https://www.cbssports.com/writers/pete-prisco/
}

breech = {
    'url': 'https://www.cbssports.com/nfl/news/nfl-week-18-picks-and-score-predictions-best-bets-odds/',
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
    'url': 'https://www.azcentral.com/story/sports/nfl/2025/12/29/nfl-week-18-picks-predictions-score-projections-2025-season/87842933007/',
    'name': 'Jeremy Cluff', # Jenna Ortiz', # 
    'searchTerm': 'Prediction:', # cluff: 'Prediction:'
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
    'url': 'https://nflspinzone.com/2025-nfl-picks-score-predictions-for-every-week-18-game-as-playoffs-approach-01kdnm2vdddw',
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
    'url': 'https://www.sportingnews.com/us/nfl/news/nfl-picks-predictions-week-18/871ee4da0eb0a67e78a84c74',
    'name': 'BillBender',
    'searchTerm': 'Pick:',
    'searchTag': 'strong',
    'separator': ', '
    # https://www.sportingnews.com/us/author/bill-bender
}

iyer = {
    'url': 'https://www.sportingnews.com/us/nfl/news/nfl-picks-predictions-against-spread-week-18/553a362f0e7dc3032c3d335c'
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
    'url': 'https://sportsnaut.com/nfl/nfl-week-' + str(weeknum) + '-predictions-nfl-picks-this-week'
    # https://sportsnaut.com/nfl/nfl-week-11-predictions-picks-nfl-schdeule-this-week
}

copilot = {
    'url': 'https://www.usatoday.com/story/sports/nfl/2026/01/01/nfl-week-18-picks-predictions-ai/87963374007/', # https://www.usatoday.com/staff/75156654007/jacob-camenker/
    'name': 'Copilot',
    'searchXPath': "//h3[@class='gnt_ar_b_h3']", #gnt_ar_b_h3
    'separator': ', '

}

usatoday = {
    'url': 'https://e.infogram.com/b29a56b9-5696-4974-9716-3320c4e81518?src=embed#async_embed' #https://e.infogram.com/ad6b49fa-d4a5-4787-b6ae-9e8592ca802a?src=embed#async_embed'
    # https://www.usatoday.com/sports/nfl/
}

espn = {
    'url': 'https://www.espn.com/nfl/story?page=viewersguide47473045&_slug_=nfl-week-18-picks-predictions-schedule-fantasy-football-odds-injuries-stats-2025'
    # https://www.espn.com/nfl/
}

nfl = {
    'url': 'https://www.nfl.com/news/nfl-picks-week-18-2025-nfl-season'
    # https://www.nfl.com/news/series/game-picks-news
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
    'url': 'https://www.rotowire.com/football/article/beating-the-book-101805', # https://www.rotowire.com/football/column/beating-the-book-20
    'name': 'NickWhalen',
    'searchTerm': 'The pick:',
    'separator': ' - '
}

rotowire2 = {
    'url': 'https://www.rotowire.com/betting/nfl/odds/week-' + str(weeknum),
    'name': 'Rotowire',
    'searchTerm': 'Final Score:',
    'separator': ' | '
}

sbr = {
    'url': 'https://www.sportsbookreview.com/picks/nfl/ai-predictions-beat-the-bot-week-' + str(weeknum) + '-2025/'
}

rotoballer = {
    'url': 'https://www.rotoballer.com/nfl-predictions-week-13-picks-and-analysis-for-every-game-2025/1765373',
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

writersArray = [ts, pp, bender, foxsports, azc,  rotowire2] #, sz, foxsports, azc, pfn, rotoballer, 
request_headers = {'User-Agent': 'Mozilla/5.0'}

errors = []
nopicks = []

# Thread-based timeout for function calls
class TimeoutError(Exception):
    pass

def run_with_timeout(func, args=(), kwargs={}, timeout=60):
    """Run a function with a timeout using threading"""
    result = [TimeoutError(f"Operation timed out after {timeout} seconds")]
    
    def target():
        try:
            result[0] = func(*args, **kwargs)
        except Exception as e:
            result[0] = e
    
    thread = threading.Thread(target=target)
    thread.daemon = True
    thread.start()
    thread.join(timeout)
    
    if thread.is_alive():
        print(f"Function timed out after {timeout} seconds")
        raise TimeoutError(f"Operation timed out after {timeout} seconds")
    
    if isinstance(result[0], Exception):
        raise result[0]
    
    return result[0]

def safe_get_url(driver, url, timeout=20):
    """Safely load a URL with timeout protection"""
    try:
        driver.set_page_load_timeout(timeout)
        driver.get(url)
        return True
    except TimeoutException:
        print(f"Timeout loading {url}, stopping page load...")
        try:
            driver.execute_script("window.stop();")
        except:
            pass
        # Even after timeout, check if page is usable
        try:
            driver.execute_script("return document.readyState");
            return True  # Page might be partially loaded but usable
        except:
            return False
    except Exception as e:
        print(f"Error loading {url}: {e}")
        return False

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
weboptions.add_argument("--disable-webgl")
weboptions.add_argument("--enable-unsafe-swiftshader")
weboptions.add_argument("--log-level=3")
weboptions.page_load_strategy = 'normal'  # Changed from 'eager' for better compatibility

driver = webdriver.Chrome(options=weboptions)

driver.set_page_load_timeout(20)  # Reduced from 30 to 20 seconds
try:
    i = 0
    for writer in writersArray:
        print('i: ', i)
        if i % 5 == 0:
            try:
                driver.quit()
            except:
                pass
            driver = webdriver.Chrome(options=weboptions)
            driver.set_page_load_timeout(20)
        if writer['url'] != '':
            print('writer[\'name\']:', writer['name'])
            
            print('getting url')
            if not safe_get_url(driver, writer['url'], timeout=20):
                print(f"Failed to load {writer['name']}, skipping...")
                nopicks.append([writer.get('name'), writer.get('url'), 'Timeout'])
                i = i + 1
                continue
            
            print('waiting')
            wait = WebDriverWait(driver, timeout=3)  # Reduced from 5 to 3 seconds
            print('done waiting')
            print('hasattr()', writer.get("searchTerm"))
            searchTerm = writer.get("searchTerm")
            searchTag = writer.get("searchTag")
            searchXPath = writer.get("searchXPath")

            try:
                if searchTerm:
                    picks = wait.until(EC.presence_of_all_elements_located(
                        (By.XPATH, "//*[contains(text(), '" + writer['searchTerm'] + "')]/parent::*")
                    ))
                elif searchTag:
                    picks = wait.until(EC.presence_of_all_elements_located(
                        (By.TAG_NAME, writer["searchTag"])
                    ))
                else:
                    picks = wait.until(EC.presence_of_all_elements_located(
                        (By.XPATH, writer["searchXPath"])
                    ))
            except TimeoutException:
                print(f"Timeout waiting for picks from {writer['name']}")
                picks = []
            # if writer['name'] == 'PetePrisco':
            #     print(response.data)
            # picks = soup.find_all(writer['searchTag'], string = writer['searchTerm']) #, attrs={'class': 'Article-content'}

            # print([t.parent.text for t in soup.findAll('strong', string="Projected score")])
            print('picks length: ', len(picks))
            if len(picks) == 0:
                print('writer with no picks: ', writer)
                nopicks.append([writer.get('name'), writer.get('url')])
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
                    except KeyboardInterrupt:
                        print(f"\nManual skip triggered! Moving to next URL...")
                        continue  # Skips the rest of this loop iteration
                    except TimeoutException:
                        print(f"Timeout processing pick from {writer['name']}, skipping...")
                        continue
                    except ValueError:
                        errors.append([writer['name'], traceback.print_exc(), ValueError])
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
                    except KeyboardInterrupt:
                        print(f"\nManual skip triggered! Moving to next URL...")
                        continue  # Skips the rest of this loop iteration
                    except ValueError:
                        errors.append([writer['name'], traceback.print_exc(), ValueError])
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
            
            print('breech: ', predictionString)
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
            except KeyboardInterrupt:
                print(f"\nManual skip triggered! Moving to next URL...")
                continue  # Skips the rest of this loop iteration
            except ValueError:
                errors.append(['JohnBreech', traceback.print_exc(), ValueError])
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
            except KeyboardInterrupt:
                print(f"\nManual skip triggered! Moving to next URL...")
                continue  # Skips the rest of this loop iteration
            except ValueError:
                errors.append(['Sportsnaut', traceback.print_exc(), ValueError])
                print(ValueError)
                
    except KeyboardInterrupt:
        print(f"\nManual skip triggered! Moving to next URL...")
    except ValueError:
        errors.append(['Breech/Sportsnaut', traceback.print_exc(), ValueError])
        print('breech ValueError:', ValueError)

    # vinnie iyer formatting
    try: 
        if not safe_get_url(driver, iyer["url"], timeout=20):
            print("Failed to load Vinnie Iyer page, skipping...")
            raise TimeoutException("Page load timeout")
        
        wait = WebDriverWait(driver, timeout=5)  # Reduced from 10 to 5
        # try:
        #     games = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "h3")))
        #     picks = wait.until(EC.presence_of_all_elements_located(
        #         (By.XPATH, "//*[contains(text(), 'Pick:')]/parent::*")
        #     ))
        # except TimeoutException:
        #     print("Timeout waiting for Iyer elements")
        #     games = []
        #     picks = []
        games = driver.find_elements(By.TAG_NAME, "h3")
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
    
    except KeyboardInterrupt:
        print(f"\nManual skip triggered! Moving to next URL...")
    except TimeoutException:
        print('Iyer timeout, skipping...')
        errors.append(['Iyer', 'Timeout', 'TimeoutException'])
    except ValueError:
        errors.append(['Iyer', traceback.print_exc(), ValueError])
        print('iyer ValueError: ', ValueError)
    except Exception as e:
        print(f'Iyer error: {e}')
        errors.append(['Iyer', str(e), 'Exception'])


    if espn['url'] is not None:
        try:
            espnrows = run_with_timeout(fetch_espn_data, args=(weeknum, espn['url'], weboptions), timeout=45)
            for espnrow in espnrows:
                rows.append(espnrow)
        except TimeoutError:
            print("ESPN scraper timed out, skipping...")
            errors.append(['ESPN', 'Timeout', 'TimeoutError'])
        except Exception as e:
            print(f"ESPN scraper error: {e}")
            errors.append(['ESPN', str(e), 'Exception'])

        # dimers formatting
        # try:
            if not safe_get_url(driver, 'https://www.dimers.com/bet-hub/nfl/schedule', timeout=20):
                print("Failed to load Dimers, skipping...")
                raise TimeoutException("Page load timeout")
            
            wait = WebDriverWait(driver, timeout=5)  # Reduced from 10 to 5
        #     driver.refresh()

        #     matchgrid = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "match-list-grid")))
        #     games = matchgrid.find_elements(By.CLASS_NAME,"game-link")    
        #     firstGame = wait.until(EC.element_to_be_clickable((By.CLASS_NAME,"game-link")))
            
        #     popup = driver.find_elements(By.CLASS_NAME, "gnt_mol_xb")
        #     if len(popup) > 0:
        #         try:
        #             wait.until(EC.element_to_be_clickable(popup[0]))
        #             popup[0].click()
        #         except TimeoutException:
        #             print("Popup close timeout, continuing...")
        #     try: 
        #         pageBlocker = driver.find_element(By.CLASS_NAME, 'ab-page-blocker')
        #         if pageBlocker is not None:
        #             closeButton = driver.find_element(By.CLASS_NAME, "ab-close-button")
        #             wait.until(EC.element_to_be_clickable(closeButton))
        #             closeButton.click()
        #     except (TimeoutException, NoSuchElementException):
        #         print('ad blocker not found or timeout')            
            
        #     try:
        #         wait.until(EC.element_to_be_clickable(firstGame))
        #         if firstGame is not None:
        #             firstGame.click()
        #     except TimeoutException:
        #         print("First game not clickable, skipping Dimers...")
        #         raise
        #         # response = requests.get()
        #         # print(response)
        #         # soup = BeautifulSoup(response.text, 'html.parser')
        #         # games = soup.find_all('h3')
        #         # picks = soup.find_all('strong', string="Pick: ") #, attrs={'class': 'Article-content'}

        #         # print([t.parent.text for t in soup.findAll('strong', string="Projected score")])
                
        #         # print('gamesObject: ', gamesObject)
        #         g = 0
        #         while g < len(games)-1: 
        #             try:
        #                 teams = wait.until(EC.presence_of_all_elements_located(
        #                     (By.CLASS_NAME, "team-column")
        #                 ))
        #             except TimeoutException:
        #                 print(f"Timeout waiting for teams at game {g}, skipping...")
        #                 g = g + 1
        #                 continue
                    
        #             if teams is not None and len(teams) > 0:
        #                 try:
        #                     scores = wait.until(EC.presence_of_all_elements_located(
        #                         (By.CLASS_NAME, "score")
        #                     ))
        #                 except TimeoutException:
        #                     print(f"Timeout waiting for scores at game {g}, skipping...")
        #                     g = g + 1
        #                     continue
        #                 awayTeam = teams[0].text
        #                 awayScore = scores[0].text
        #                 homeTeam = teams[1].text
        #                 homeScore = scores[1].text
                        
                        
        #                 print('awayTeam, awayScore, homeTeam, homeScore: ', awayTeam, awayScore, homeTeam, homeScore)
        #                 if awayScore > homeScore:
        #                     winner = awayTeam
        #                     winnerScore = awayScore
        #                     loser = homeTeam
        #                     loserScore = homeScore
        #                 else:
        #                     winner = homeTeam
        #                     winnerScore = homeScore
        #                     loser = awayTeam
        #                     loserScore = awayScore    
                            
        #                 rows.append(['Dimers',winner, int(winnerScore), loser, int(loserScore)])
        #                 try:
        #                     navButtons = wait.until(EC.presence_of_all_elements_located(
        #                         (By.CLASS_NAME,"match-nav-link")
        #                     ))
        #                     if len(navButtons) > 1:
        #                         wait.until(EC.element_to_be_clickable(navButtons[1]))
        #                         navButtons[1].click()
        #                         # Give a moment for page to update, but don't wait for staleness
        #                         import time
        #                         time.sleep(1)
        #                 except (TimeoutException, StaleElementReferenceException) as e:
        #                     print(f"Navigation error at game {g}: {e}")
        #                 g = g + 1
        #                 print('g:', g)
        #             else:
        #                 g = g + 1
                    
        # except KeyboardInterrupt:
        #     print(f"\nManual skip triggered! Moving to next URL...")
        # except TimeoutException:
        #     print("Dimers timeout, skipping...")
        #     errors.append(['Dimers', 'Timeout', 'TimeoutException'])
        # except ValueError:
        #     print(ValueError)
        #     print(['dimers',winner, winnerScore, loser, loserScore])
        #     rows.append(['dimers',winner, winnerScore, loser, loserScore])
        # except Exception as e:
        #     print(f"Dimers error: {e}")
        #     errors.append(['Dimers', str(e), 'Exception'])


    # usatoday formatting
    try:
        usatodayrows = run_with_timeout(fetch_usatoday_data, args=(weeknum, usatoday['url']), timeout=45)
        for usatodayrow in usatodayrows:
            rows.append(usatodayrow)
    except TimeoutError:
        print("USA Today scraper timed out, skipping...")
        errors.append(['USAToday', 'Timeout', 'TimeoutError'])
    except Exception as e:
        print(f"USA Today error: {e}")
        errors.append(['USAToday', str(e), 'Exception'])

    # nfl formatting
    try:
        nflrows = run_with_timeout(fetch_nfl_data, args=(weeknum, nfl['url'], weboptions), timeout=45)
        for nflrow in nflrows:
            rows.append(nflrow)
    except TimeoutError:
        print("NFL scraper timed out, skipping...")
        errors.append(['NFL', 'Timeout', 'TimeoutError'])
    except Exception as e:
        print(f"NFL error: {e}")
        errors.append(['NFL', str(e), 'Exception'])

    try:
        oddssharkrows = run_with_timeout(fetch_oddsshark_data, args=(weeknum, weboptions), timeout=45)
        for oddssharkrow in oddssharkrows:
            rows.append(oddssharkrow)
    except TimeoutError:
        print("OddsShark timed out, skipping...")
        errors.append(['OddsShark', 'Timeout', 'TimeoutError'])
    except Exception as e:
        print(f"OddsShark error: {e}")
        errors.append(['OddsShark', str(e), 'Exception'])
        
    try:
        dratingsrows = run_with_timeout(fetch_dratings_data, args=(weeknum, weboptions), timeout=45)
        for dratingsrow in dratingsrows:
            rows.append(dratingsrow)
    except TimeoutError:
        print("DRatings timed out, skipping...")
        errors.append(['DRatings', 'Timeout', 'TimeoutError'])
    except Exception as e:
        print(f"DRatings error: {e}")
        errors.append(['DRatings', str(e), 'Exception'])

    try:
        oddstraderrows = run_with_timeout(fetch_oddstrader_data, args=(weeknum, weboptions), timeout=45)
        for oddstraderrow in oddstraderrows:
            rows.append(oddstraderrow)
    except TimeoutError:
        print("OddsTrader timed out, skipping...")
        errors.append(['OddsTrader', 'Timeout', 'TimeoutError'])
    except Exception as e:
        print(f"OddsTrader error: {e}")
        errors.append(['OddsTrader', str(e), 'Exception'])

    try:
        nflspinzonerows = run_with_timeout(fetch_nflspinzone_data, args=(sz['url'], weeknum, weboptions), timeout=45)
        for nflspinzonerow in nflspinzonerows:
            rows.append(nflspinzonerow)
    except TimeoutError:
        print("NFL Spinzone timed out, skipping...")
        errors.append(['NFLSpinzone', 'Timeout', 'TimeoutError'])
    except Exception as e:
        print(f"NFL Spinzone error: {e}")
        errors.append(['NFLSpinzone', str(e), 'Exception'])

    try:
        sbrrows = run_with_timeout(fetch_sbr_data, args=(weeknum, sbr['url'], weboptions), timeout=45)
        for sbrrow in sbrrows:
            rows.append(sbrrow)
    except TimeoutError:
        print("SBR timed out, skipping...")
        errors.append(['SBR', 'Timeout', 'TimeoutError'])
    except Exception as e:
        print(f"SBR error: {e}")
        errors.append(['SBR', str(e), 'Exception'])

    try:
        clutchpointsrows = run_with_timeout(fetch_clutchpoints_data, args=(weeknum, clutchpoints['url'], weboptions), timeout=45)
        for clutchpointsrow in clutchpointsrows:
            rows.append(clutchpointsrow)
    except TimeoutError:
        print("ClutchPoints timed out, skipping...")
        errors.append(['ClutchPoints', 'Timeout', 'TimeoutError'])
    except Exception as e:
        print(f"ClutchPoints error: {e}")
        errors.append(['ClutchPoints', str(e), 'Exception'])

    try:
        copilotrows = run_with_timeout(fetch_copilot_data, args=(weeknum, copilot['url'], weboptions), timeout=45)
        for copilotrow in copilotrows:
            rows.append(copilotrow)
    except TimeoutError:
        print("Copilot timed out, skipping...")
        errors.append(['Copilot', 'Timeout', 'TimeoutError'])
    except Exception as e:
        print(f"Copilot error: {e}")
        errors.append(['Copilot', str(e), 'Exception'])
    
    try:
        rotowirerows = run_with_timeout(fetch_rotowire_data, args=(weeknum, rotowire['url'], weboptions), timeout=45)
        for rotowirerow in rotowirerows:
            rows.append(rotowirerow)
    except TimeoutError:
        print("Rotowire timed out, skipping...")
        errors.append(['Rotowire', 'Timeout', 'TimeoutError'])
    except Exception as e:
        print(f"Rotowire error: {e}")
        errors.append(['Rotowire', str(e), 'Exception'])


except KeyboardInterrupt:
    print(f"\nManual skip triggered! Moving to next URL...")
except Exception as e:    
    print(f"Unexpected error: {e}")
finally:
    # Ensure driver is closed properly
    if 'driver' in locals():
        try:
            driver.quit()
        except Exception as cleanup_error:
            # Log but don't raise - we're already in cleanup
            print(f"Warning: Error during driver cleanup: {cleanup_error}")
    
    # Write results to CSV file
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
        csvwriter.writerows(nopicks)
# finally:
#     # Always clean up the driver
#     try:
#         driver.quit()
#         print("Driver closed successfully")
#     except:
#         pass
# # print(picks)
