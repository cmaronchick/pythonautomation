# Python script for web scraping to extract data from a website
import requests, sys, datetime, urllib3
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
import csv, docx, traceback
from docx import Document
import urllib3.request

ts = {
    'url': 'https://www.cbssports.com/nfl/news/nfl-week-4-odds-picks-best-bets-steelers-stay-perfect-with-win-in-indy-rams-upset-bears-in-chicago/',
    'name': 'TerrySullivan',
    'searchTerm': 'Projected score',
    'searchTag': 'strong',
    'endPickTerm': 'The pick:',
    'separator': ', '
    # https://www.cbssports.com/writers/tyler-sullivan/
}
pp = {
    'url': 'https://www.cbssports.com/nfl/news/pete-priscos-week-4-nfl-picks-ravens-cool-off-unbeaten-bills-packers-hand-vikings-first-loss/',
    'name': 'PetePrisco',
    'searchTerm': 'Pick:',
    'searchTag': 'strong',
    'separator': ', '
    #https://www.cbssports.com/writers/pete-prisco/
}

foxsports = {
    'url': 'https://www.foxsports.com/articles/nfl/2024-nfl-week-4-predictions-betting-odds-tv-schedule',
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
    'url': 'https://www.profootballnetwork.com/week-4-nfl-picks-predictions-2024/',
    'name': 'PFN',
    'searchTerm': 'Prediction:',
    'searchTag': 'strong',
    'separator': ', '
    # https://www.profootballnetwork.com/author/brolfe/
}

sz = {
    'url': 'https://nflspinzone.com/posts/2024-nfl-picks-score-predictions-for-week-4-games-01j8fna52mnw',
    'name': 'NFL Spinzone',
    'searchTerm': 'Prediction:',
    'searchTag': 'strong',
    'separator': ', '
}

cowherd = {
    'url': 'https://foxsportsradio.iheart.com/featured/the-herd-with-colin-cowherd/content/2024-09-06-blazing-five-colin-cowherd-gives-his-5-best-nfl-bets-for-week-1-sep-8/',
    'name': 'ColinCowherd',
    'searchTerm': "prediction:",
    'searchTag': 'em',
    'separator': ', '
}

bleacher = {
    'url': 'https://bleacherreport.com/articles/10136706-bleacher-reports-week-4-nfl-picks',
    'name': 'BleacherReport',
    'searchTerm': 'Score Prediction:',
    'searchTag': 'b',
    'separator': ', '
}

breech = {
    'url': 'https://www.cbssports.com/nfl/news/nfl-week-4-picks-ravens-shock-undefeated-bills-raiders-top-browns-falcons-beat-saints-in-thriller/',
    'name': 'JohnBreech',
    'searchTerm': 'The pick:',
    'searchTag': 'strong',
    'separator': ' over '
    # https://www.cbssports.com/writers/john-breech/
}

bender = {
    'url': 'https://www.sportingnews.com/us/nfl/news/nfl-picks-predictions-week-4-straight-vikings-bills/11a57cad6fbfa3f125c16478',
    'name': 'BillBender',
    'searchTerm': 'Pick:',
    'searchTag': 'strong',
    'separator': ', '
    # https://www.sportingnews.com/us/author/bill-bender
}

iyer = {
    'url': 'https://www.sportingnews.com/us/nfl/news/nfl-picks-predictions-against-spread-week-4-cowboys-chiefs/babdc8e304317864905e3647'
}

thirtythirdteam = {
    'url': 'https://www.the33rdteam.com/2024-nfl-week-4-expert-picks-predictions-for-every-game/',
    'name': 'MarcusMosher',
    'searchTerm': 'Score Prediction:',
    'searchTag': 'strong',
    'separator': ', '

}

writersArray = [ts, pp, bleacher, bender, pfn, breech, sz, foxsports, thirtythirdteam] #, foxsports, azc, 
request_headers = {'User-Agent': 'Mozilla/5.0'}

chrome_driver_path = './chromedriver'


weeknum = 4

# article = driver.find_element(By.CLASS_NAME, "Article-content")
# picks = driver.find_element(By.TAG_NAME, "strong")
rows = []
chrome_driver_path = './chromedriver'

service = Service(chrome_driver_path)
weboptions = webdriver.ChromeOptions()
weboptions.accept_insecure_certs = True
driver = webdriver.Chrome(options=weboptions)
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
            print(colonIndex, pickIndex)
            if colonIndex == -1:
                print(p)
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
                loserScore = predictionString[secondSpace:]
                # print([writer['name'],winner, winnerScore, loser, loserScore])
                try:
                    rows.append([writer['name'],winner, int(winnerScore), loser, int(loserScore)])
                except ValueError:
                    print(ValueError, [writer['name'],winner, winnerScore, loser, loserScore])
                # print(winner, int(winnerScore), loser, int(loserScore))

    # # sportsnaut formatting

    response = requests.get('https://sportsnaut.com/list/nfl-week-4-predictions-2024/')
    print(response)
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
        awayTeam = gameString[colonIndex+addedSpaces:firstSpace].strip()
        gamesObject[homeTeam] = {
            "awayTeam": awayTeam,
            "homeTeam": homeTeam
        }
        
        gamesObject[awayTeam] = {
            "awayTeam": awayTeam,
            "homeTeam": homeTeam
        }
    # print('gamesObject: ', gamesObject)
    print('VI picks:', len(picks))
    for p in picks:
        #Texans win 20-17 and cover the spread.
        predictionString = p.text
        colonIndex = predictionString.find(":")
        scoreSeparatorIndex = predictionString.find("-")
        firstSpace = predictionString.find(" ",colonIndex+2)
        winningTeam = predictionString[colonIndex+2:firstSpace]
        separator = predictionString.find(" win ")
        winnerScore = predictionString[separator+len(" win "):scoreSeparatorIndex]
        lastSpace = predictionString.find(" ",scoreSeparatorIndex)
        loserScore = predictionString[scoreSeparatorIndex+1:lastSpace]
        print('winningTeam, winningScore, losingScore', winningTeam, winnerScore, loserScore)
        
        winner = None
        loser = None
        if winningTeam != "Vinnie":
            if gamesObject[winningTeam]["awayTeam"] == winningTeam:
                winner = gamesObject[winningTeam]["awayTeam"]
                loser = gamesObject[winningTeam]["homeTeam"]
            else:
                winner = gamesObject[winningTeam]["homeTeam"]
                loser = gamesObject[winningTeam]["awayTeam"]
        print(['VinnieIyer',winner, int(winnerScore), loser, int(loserScore)])
        rows.append(['VinnieIyer',winner, int(winnerScore), loser, int(loserScore)])

    # dimers formatting
    driver.get('https://www.dimers.com/bet-hub/nfl/schedule')
    wait = WebDriverWait(driver, timeout=2)
    driver.implicitly_wait(10)
    # resultsTable = driver.find_elements_by_xpath("//*[contains(text(), " + writer['searchTerm'] + ")]")
    # wait.until(lambda d : resultsTable.is_displayed())
    matchgrid = driver.find_element(By.CLASS_NAME, "match-list-grid")
    games = matchgrid.find_elements(By.CLASS_NAME,"game-link")
    firstGame = matchgrid.find_element(By.CLASS_NAME,"game-link")
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
            g = g + 1
            print('g:', g)
        else:
            g = g + 1

    # usatoday formatting

    driver.get('https://www.usatoday.com/story/sports/nfl/2024/09/25/dallas-cowboys-new-york-giants-picks-predictions-odds-week-4/75300481007/')
    wait = WebDriverWait(driver, timeout=2)
    # driver.implicitly_wait(10)
    # resultsTable = driver.find_elements_by_xpath("//*[contains(text(), " + writer['searchTerm'] + ")]")
    articleBody = driver.find_element(By.TAG_NAME, "article")
    pickLinkIndex = 0
    wait.until(lambda d : articleBody.is_displayed())
    pickLinks = articleBody.find_elements(By.XPATH,'//a[contains(text(), " vs. ")]')    # pickLinks2 = driver.find_elements(By.XPATH, "/html/body/div[3]/main/article/div[5]/p[10]/a")
    print(len(pickLinks))
    while pickLinkIndex < len(pickLinks):
        pickLinks[pickLinkIndex].click()
        articleBody = driver.find_element(By.TAG_NAME, "article")
        wait.until(lambda d : articleBody.is_displayed())
        title = driver.find_element(By.TAG_NAME, "h1")
        wait.until(lambda d : title.is_displayed())
        headers = driver.find_elements(By.TAG_NAME, "h2")
        headerIndex = 0
        for header in headers:
            if headerIndex > 1:
                separatorIndex = header.text.find(":")
                author = header.text[:separatorIndex].replace(" ","")
                winner = header.text[separatorIndex+2:header.text.find(",")].split(" ")
                winningTeam = winner[0]
                winningScore = winner[1]
                loser = header.text[header.text.find(",")+2:].split(" ")
                losingTeam = loser[0]
                losingScore = loser[1]
                print('author:', author, winningTeam, winningScore, losingTeam, losingScore)
                rows.append([author,winningTeam, winningScore, losingTeam, losingScore])                    
            headerIndex = headerIndex + 1
        pickLinkIndex = pickLinkIndex + 1 
        driver.get('https://www.usatoday.com/story/sports/nfl/2024/09/25/dallas-cowboys-new-york-giants-picks-predictions-odds-week-4/75300481007/')
        popup = driver.find_elements(By.CLASS_NAME, "gnt_mol_xb")
        if len(popup) > 0:
            popup[0].click()
        articleBody = driver.find_element(By.TAG_NAME, "article")
        wait.until(lambda d : articleBody.is_displayed())

        pickLinks = articleBody.find_elements(By.XPATH,'//a[contains(text(), " vs. ")]')
        print(len(pickLinks))
        
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
