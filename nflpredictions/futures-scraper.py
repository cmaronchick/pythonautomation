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

year = 2025
season = "post"
weeknum = 4


bmr = {
    'url': 'https://odds.bookmakersreview.com/nfl/futures/',
}

request_headers = {'User-Agent': 'Mozilla/5.0'}




# article = driver.find_element(By.CLASS_NAME, "Article-content")
# picks = driver.find_element(By.TAG_NAME, "strong")
chrome_driver_path = '../chromedriver'

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

driver = webdriver.Chrome(weboptions)
try:
    
    books = []
    driver.get(bmr['url'])
    wait = WebDriverWait(driver, timeout=2)
    driver.implicitly_wait(10)
    # resultsTable = driver.find_elements_by_xpath("//*[contains(text(), " + writer['searchTerm'] + ")]")
    # wait.until(lambda d : resultsTable.is_displayed())

    table = driver.find_element(By.TAG_NAME, "table")
    tableheader = table.find_element(By.TAG_NAME, "thead")
    headercolumns = tableheader.find_elements(By.TAG_NAME, "th")
    print('th:', len(headercolumns))
    headerindex = 0
    for header in headercolumns:
        if headerindex == 0:
            headerindex = headerindex + 1
            continue
        if headerindex == 1:
            books.append(header.text)
            headerindex = headerindex + 1
            continue
        link = header.find_element(By.TAG_NAME, "a")
        linkText = link.text
        images = link.find_elements(By.TAG_NAME, "img")
        print('images:', len(images))
        image = images[0]
        # attrs = driver.execute_script('var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) { items[arguments[0].properties[index].name] = arguments[0].properties[index].value }; return items;', image)
        # print(attrs)
        # //*[@id="main-content"]/div[2]/table/thead/tr/th[3]/a/img
        print('image:', link.tag_name, linkText, image.get_attribute('alt'))
        books.append(image.get_attribute("alt"))
    print('books:', books)
    tablebody = table.find_element(By.TAG_NAME, "tbody")
    rows = tablebody.find_elements(By.TAG_NAME, "tr")
    teamodds = []
    for row in rows:
        columns = row.find_elements(By.TAG_NAME, "td")
        team = columns[0].text
        print('team: ', team)
        columnIndex = 0
        odds = []
        for column in columns:
            if columnIndex == 0:
                continue
            odds.append(column.text())
        teamodds[team] = odds

    print('teamodds: ', teamodds)


    #find_elements_by_xpath("//*[contains(text(), " + writer['searchTerm'] + ")]")
    # if writer['name'] == 'PetePrisco':
    #     print(response.data)
    # picks = soup.find_all(writer['searchTag'], string = writer['searchTerm']) #, attrs={'class': 'Article-content'}

    # print([t.parent.text for t in soup.findAll('strong', string="Projected score")])
    # print('picks length: ', len(rows))
    # for p in picks:
    #     # parent = p.parent.text        
    #     # colonIndex = parent.find(':')
    #     pText = p.text
    #     # print('p:', pText)
    #     colonIndex = pText.find(':')
    #     pickIndex = None
    #     if "endPickTerm" in writer:
    #         pickIndex = pText.find(writer['endPickTerm'])
    #     print('195', colonIndex, pickIndex)
    #     if colonIndex == -1:
    #         print('pick: ', p)
    #     if (colonIndex > 0):
    #         predictionString = ""
    #         if pickIndex is not None:
    #             predictionString = pText[colonIndex+2:pickIndex]
    #         else:
    #             predictionString = pText[colonIndex+2:]
    #         firstSpace = predictionString.find(" ")
    #         separator = predictionString.find(writer['separator'])
    #         secondSpace = predictionString.find(" ", separator+len(writer['separator']))
    #         winner = predictionString[:firstSpace]
    #         winnerScore = predictionString[firstSpace:separator]
    #         loser = predictionString[separator+2:secondSpace]
    #         loserScore = predictionString[secondSpace:].strip()
    #         # print([writer['name'],winner, winnerScore, loser, loserScore])
    #         try:
    #             rows.append([writer['name'],winner, int(winnerScore), loser, int(loserScore)])
    #         except ValueError:
    #             print(ValueError, [writer['name'],winner, winnerScore, loser, loserScore])
    #             # print(winner, int(winnerScore), loser, int(loserScore))

    
    ### Final Row for printing picks ###
    week1picks = open(str(year) + season + "week" + str(weeknum) + "futures.csv", 'w+', newline='')
    with week1picks as csvfile:
        
        # creating a csv writer object  
        csvwriter = csv.writer(csvfile)  
            
        # writing the fields  
        
        fields = ['Source', 'Winner', 'Winner Score', 'Loser', 'Loser Score']
        csvwriter.writerow(fields)  
            
        # writing the data rows  
        csvwriter.writerows(teamodds) 
except:    
    print(traceback.print_exc())
    week1picks = open(str(year) + season + "week" + str(weeknum) + "futures.csv", 'w+', newline='')
    with week1picks as csvfile:
        
        # creating a csv writer object  
        csvwriter = csv.writer(csvfile)  
            
        # writing the fields  
        
        fields = ['Source', 'Winner', 'Winner Score', 'Loser', 'Loser Score']
        csvwriter.writerow(fields)  
            
        # writing the data rows  
        csvwriter.writerows(teamodds) 
# print(picks)
