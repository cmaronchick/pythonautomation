# Python script for web scraping to extract data from a website
import requests, sys, datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
import csv, docx
from docx import Document

ts = {
    'url': 'https://www.cbssports.com/nfl/news/nfl-week-1-odds-picks-c-j-stroud-texans-start-2024-season-with-road-win-packers-pull-off-upset-in-brazil/',
    'name': 'TerrySullivan',
    'searchTerm': 'Projected score',
    'endPickTerm': 'The pick:'
    
}
pp = {
    'url': 'https://www.cbssports.com/nfl/news/priscos-week-1-nfl-picks-jordan-love-led-packers-torch-eagles-defense-jaguars-win-shootout-in-miami/',
    'name': 'PetePrisco',
    'searchTerm': 'Pick:'
}

sz = {
    'url': 'https://nflspinzone.com/posts/2024-nfl-picks-score-predictions-for-week-1-01j6sk7gzgpn',
    'name': 'SayreBedinger',
    'searchTerm': 'Prediction:'
}

writersArray = [ts, pp]

chrome_driver_path = './chromedriver'

# service = Service(chrome_driver_path)
# driver = webdriver.Chrome()
# driver.get(url)
# wait = WebDriverWait(driver, timeout=2)
# article = driver.find_element(By.CLASS_NAME, "Article-content")
# picks = driver.find_element(By.TAG_NAME, "strong")
rows = []
for writer in writersArray:
    
    response = requests.get(writer['url'])
    print(response)
    soup = BeautifulSoup(response.text, 'html.parser')
    picks = soup.find_all('strong', string = writer['searchTerm']) #, attrs={'class': 'Article-content'}

    # print([t.parent.text for t in soup.findAll('strong', string="Projected score")])
    
    for p in picks:
        parent = p.parent.text
        colonIndex = parent.find(':')
        
        pickIndex = None
        if "endPickTerm" in writer:
            pickIndex = parent.find(writer['endPickTerm'])
        print(colonIndex, pickIndex)
        if (colonIndex > 0):
            predictionString = ""
            if pickIndex is not None:
                predictionString = parent[colonIndex+2:pickIndex]
            else:
                predictionString = parent[colonIndex+2:]
            firstSpace = predictionString.find(" ")
            separator = predictionString.find(", ")
            secondSpace = predictionString.find(" ", separator+2)
            winner = predictionString[:firstSpace]
            winnerScore = predictionString[firstSpace:separator]
            loser = predictionString[separator+2:secondSpace]
            loserScore = predictionString[secondSpace:]
            # print([writer['name'],winner, winnerScore, loser, loserScore])
            rows.append([writer['name'],winner, int(winnerScore), loser, int(loserScore)])
            # print(winner, int(winnerScore), loser, int(loserScore))

# sportsnaut formatting

response = requests.get('https://sportsnaut.com/list/nfl-week-1-predictions-2024/')
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
    rows.append(['Sportsnaut',winner, int(winnerScore), loser, int(loserScore)])
week1picks = open("2024week1picks.csv", 'w+', newline='')
with week1picks as csvfile:
    
    # creating a csv writer object  
    csvwriter = csv.writer(csvfile)  
        
    # writing the fields  
    
    fields = ['Source', 'Winner', 'Score', 'Loser', 'Score']
    csvwriter.writerow(fields)  
        
    # writing the data rows  
    csvwriter.writerows(rows) 

# print(picks)
