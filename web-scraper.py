# Python script for web scraping to extract data from a website
import requests, sys
from bs4 import BeautifulSoup

url = sys.argv[1]
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
picks = soup.find_all('p' and 'strong')

for p in picks: 
    print(p, p.parent)
    # p.parent
    # split the string at the '-'
    
# Your code here to extract relevant data from the website

