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

url = 'https://www.cbssports.com/nfl/news/nfl-week-1-odds-picks-c-j-stroud-texans-start-2024-season-with-road-win-packers-pull-off-upset-in-brazil/'

chrome_driver_path = './chromedriver'

# service = Service(chrome_driver_path)
# driver = webdriver.Chrome()
# driver.get(url)
# wait = WebDriverWait(driver, timeout=2)
# article = driver.find_element(By.CLASS_NAME, "Article-content")
# picks = driver.find_element(By.TAG_NAME, "strong")

response = requests.get(url)
print(response)
soup = BeautifulSoup(response.text, 'html.parser')
picks = soup.find_all('strong', string = "Projected score") #, attrs={'class': 'Article-content'}

# print([t.parent.text for t in soup.findAll('strong', string="Projected score")])
rows = []
for p in picks:
    parent = p.parent.text
    colonIndex = parent.find(':')
    pickIndex = parent.find('The pick')
    if (colonIndex > 0):
        predictionString = parent[colonIndex+2:pickIndex]
        firstSpace = predictionString.find(" ")
        separator = predictionString.find(", ")
        secondSpace = predictionString.find(" ", separator+2)
        winner = predictionString[:firstSpace]
        winnerScore = predictionString[firstSpace:separator]
        loser = predictionString[separator+2:secondSpace]
        loserScore = predictionString[secondSpace:]
        rows.append([winner, winnerScore, loser, loserScore])
        # print(winner, int(winnerScore), loser, int(loserScore))


week1picks = open("2024week1picks.csv", 'w+')
with week1picks as csvfile:
    
    # creating a csv writer object  
    csvwriter = csv.writer(csvfile)  
        
    # writing the fields  
    
    fields = ['Winner', 'Score', 'Loser', 'Score']
    csvwriter.writerow(fields)  
        
    # writing the data rows  
    csvwriter.writerows(rows) 

# print(picks)
