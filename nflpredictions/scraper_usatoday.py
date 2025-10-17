# Python script for web scraping to extract data from a website
import sys, re, traceback, requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from bs4 import BeautifulSoup


# Setup the Chrome WebDriver

imageTable = {
    'https://images.jifo.co/21540751_1589234381582.png': 'Steelers',
    'https://images.jifo.co/21540751_1589234309546.png': 'Chiefs',
    'https://images.jifo.co/21540751_1589234633468.png': 'Ravens',
    'https://images.jifo.co/21540751_1589234284171.png': 'Chargers', #https://images.jifo.co/21540751_1589234284171.png
    'https://images.jifo.co/21540751_1589234903354.png': 'Patriots',
    'https://images.jifo.co/21540751_1589234344689.png': 'Broncos',
    'https://images.jifo.co/21540751_1589234683953.png': 'Bengals',
    'Entity_1599884617535.png': 'Rams',
    'Entity_1569032080155.png': 'Cardinals',
    'https://images.jifo.co/21540751_1589234794134.png': 'Titans',
    'Entity_1569032073772.png': 'Jaguars',
    'https://images.jifo.co/21540751_1589235745366.png': 'Buccaneers',
    'Entity_1569032073400.png': 'Colts',
    'https://images.jifo.co/21540751_1589234329160.png': 'Raiders',
    'https://images.jifo.co/21540751_1589235648280.png': 'Saints',
    'https://images.jifo.co/21540751_1589234933718.png': 'Bills',
    'https://images.jifo.co/21540751_1589235782787.png': 'Eagles',
    'Entity_1569032072269.png': 'Browns',
    'https://images.jifo.co/21540751_1589235026280.png': 'Dolphins',
    'https://images.jifo.co/21540751_1589235378659.png': 'Vikings',
    'https://images.jifo.co/21540751_1589235547463.png': 'Packers',
    'https://images.jifo.co/21540751_1589235620028.png': 'Falcons',
    'https://images.jifo.co/21540751_1652361392787.png': 'Commanders',
    'https://images.jifo.co/21540751_1589235580554.png': 'Lions',
    'https://images.jifo.co/21540751_1652361392655.png': 'Rams',
    'https://images.jifo.co/21540751_1589235820974.png': 'Cowboys',
    'https://images.jifo.co/21540751_1589234722688.png': 'Colts',
    'https://images.jifo.co/21540751_1589236085652.png': 'Seahawks',
    'https://images.jifo.co/21540751_1589234758244.png': 'Jaguars',
    'https://images.jifo.co/21540751_1757107639027.png': 'Browns',
    'https://images.jifo.co/21540751_1589235427498.png': 'Bears',
    'https://images.jifo.co/21540751_1721324476152.png': 'Jets',
    'https://images.jifo.co/21540751_1589235730471.png': 'Panthers',
    'https://images.jifo.co/21540751_1589235220318.png': '49ers',
    'https://images.jifo.co/21540751_1589234832987.png': 'Texans'
}

articleTable = [
    {"DALPHI": "https://sportsbookwire.usatoday.com/story/sports/nfl/2025/09/03/cowboys-at-eagles-odds-picks-and-predictions/83524137007/"},
    
]

chrome_driver_path = './chromedriver'

service = Service(chrome_driver_path)
weboptions = webdriver.ChromeOptions()
weboptions.accept_insecure_certs = True
weboptions.add_argument('--ignore-certificate-errors')
weboptions.add_argument('disable-notifications')
weboptions.page_load_strategy = 'eager'
driver = webdriver.Chrome(options=weboptions)
def fetch_usatoday_data(weeknum, url):
    print('fetch_usatoday_data:', url)
    usatodayrows = []
    try:
        # usatoday formatting
        driver.get(url)
        wait = WebDriverWait(driver, timeout=2)
        driver.implicitly_wait(3)
        writersText = []
            
        # original_window = driver.current_window_handle
        # windowhandles = len(driver.window_handles)
        # resultsTable = driver.find_elements_by_xpath("//*[contains(text(), " + writer['searchTerm'] + ")]")
        
        # articleBody = driver.find_element(By.TAG_NAME, "article")
        if url.find("tallysight") > -1:            
            table = driver.find_element(By.TAG_NAME, "table")
            wait.until(lambda d : table.is_displayed())
            writers = table.find_elements(By.TAG_NAME, "th")
            
            writersText = []
            writerIndex = 0
            for writer in writers:
                writersText.append({ "name": re.sub(r'\s+', '', writer.text), "prediction": "", "index": writerIndex})
                writerIndex = writerIndex + 1
            print('writersText:', writersText)
            # use for tallysight URL
            tableBody = table.find_element(By.TAG_NAME, "tbody")
            tableRows = tableBody.find_elements(By.TAG_NAME, "tr")
                # specialOffer = driver.find_elements(By.CSS_SELECTOR, "iframe[title='Special offer']")
                # if len(specialOffer) > 0:
                #     # articleBody.send_keys(Keys.ESCAPE)
                #     driver.switch_to
            print(len(tableRows))
            for tableRow in tableRows:
                columnIndex = 0
                columns = tableRow.find_elements(By.TAG_NAME, "td")
                awayTeam = ""
                homeTeam = ""
                for column in columns:
                    if columnIndex == 0:
                        teamSpans = column.find_elements(By.TAG_NAME, "span")
                        awayTeam = teamSpans[0].text
                        homeTeam = teamSpans[1].text
                        print(awayTeam, homeTeam)
                    else:
                        spans = column.find_elements(By.TAG_NAME, "span")
                        print(len(spans))
                        if len(spans) == 1:
                            print(spans[0].text)
                            continue
                        winningTeam = None
                        losingScore = None
                        losingTeam = None
                        winningTeam = spans[0].text.strip()
                        score = spans[1].text
                        winningScore = score[:score.find("-")].strip()
                        losingScore = score[score.rfind("-")+1:].strip()
                        if winningTeam == awayTeam:
                            losingTeam = homeTeam
                        else:
                            losingTeam = awayTeam
                        author = writersText[columnIndex-1]["name"]

                        
                        print('author:', author, winningTeam, winningScore, losingTeam, losingScore)
                        usatodayrows.append([author,winningTeam, winningScore, losingTeam, losingScore])
                    columnIndex = columnIndex + 1
        elif url.find("infogram") > -1:
            table = driver.find_element(By.TAG_NAME, "table")
            wait.until(lambda d : table.is_displayed())
            writers = table.find_elements(By.TAG_NAME, "th")
            
            writersText = []
            writerIndex = 0
            for writer in writers:
                writersText.append({ "name": re.sub(r'\s+', '', writer.text), "prediction": "", "index": writerIndex})
                writerIndex = writerIndex + 1
            print('writersText:', writersText)
            # use for tallysight URL
            tableBody = table.find_element(By.TAG_NAME, "tbody")
            tableRows = tableBody.find_elements(By.TAG_NAME, "tr")
            rowIndex = 0
            predictions = []
            currentGame = None
            for tableRow in tableRows:
                columnIndex = 0
                # rows are paired so you need an index to identify the first of two rows
                columns = tableRow.find_elements(By.TAG_NAME, "td")
                awayTeam = ""
                homeTeam = ""
                winningTeam = None
                losingTeam = None
                winningScore = None
                losingScore = None
                predictionRow = False
                print('columns:', len(columns))
                for column in columns:
                    print('rowIndex:', rowIndex, 'columnIndex:', columnIndex, column.text.find(" at "))
                    if rowIndex == 0:
                        if columnIndex == 0:
                            if column.text.find(" at ") > -1:

                                predictionRow = True
                                teamSpans = column.find_element(By.TAG_NAME, "span")
                                openParenthesis = teamSpans.text.find("(")
                                closeParenthesis = teamSpans.text.find(")")
                                separator = teamSpans.text.find(" at ")
                                awayTeam = ""
                                homeTeam = ""
                                if openParenthesis > separator:
                                    awayTeam = teamSpans.text[:separator]
                                    homeTeam = teamSpans.text[separator+4:openParenthesis-1]
                                else:
                                    awayTeam = teamSpans.text[:openParenthesis-1]
                                    homeTeam = teamSpans.text[separator+4:]
                                print(awayTeam, homeTeam)
                        else:
                            if predictionRow == True:
                                teamImage = column.find_element(By.TAG_NAME, "img")
                                teamImageSrc = teamImage.get_attribute("src")
                                # print('teamImageSrc:', imageTable, teamImageSrc)
                                winningTeam = imageTable[teamImageSrc]
                                if winningTeam == awayTeam:
                                    losingTeam = homeTeam
                                else:
                                    losingTeam = awayTeam
                                print('winningTeam:', winningTeam, 'losingTeam:', losingTeam)
                                author = writersText[columnIndex-1]["name"] 
                                predictions.append({"author": author,"winningTeam": winningTeam, "losingTeam": losingTeam})
                        if predictionRow == True and columnIndex == len(columns)-1:
                            rowIndex = 1
                        columnIndex = columnIndex + 1
                    elif rowIndex == 1:
                        scoreSeparator = column.text.find("-")
                        if scoreSeparator > -1:
                            winningScore = column.text[:scoreSeparator].strip()
                            losingScore = column.text[scoreSeparator+1:].strip()
                            print('winningScore:', winningScore, 'losingScore:', losingScore)
                            predictions[columnIndex-1]["winningScore"] = winningScore
                            predictions[columnIndex-1]["losingScore"] = losingScore
                            print('predictions:', predictions)
                            if columnIndex == len(columns)-1:
                                for prediction in predictions:
                                    print('author:', prediction["author"], prediction["winningTeam"], prediction["winningScore"], prediction["losingTeam"], prediction["losingScore"])
                                    usatodayrows.append([prediction["author"], prediction["winningTeam"], prediction["winningScore"], prediction["losingTeam"], prediction["losingScore"]])
                                    predictions = []
                                rowIndex = 0
                        columnIndex = columnIndex + 1
        elif url.find('sportsdata') > -1:
            print('trying sportsdata', url)
            try:
                mainDiv = driver.find_element(By.ID, "__next")
                print('mainDiv: ', mainDiv.text)
                wait.until(lambda d : mainDiv.is_displayed())
                picks = mainDiv.find_elements(By.XPATH, "//*[contains(text(), 'Projected scoring')]")
                print ('picks:', len(picks))

                currentGame = None
                for p in picks:
                    parentDiv = p.find_element(By.XPATH, '..')
                    parentElements = parentDiv.find_element(By.XPATH, '..')
                    print('parent elements: ', parentElements.text)
                    if parentElements is not None:
                        awayTeamDiv = parentElements[0]
                        homeTeamDiv = parentElements[2]
                        print('awayTeamDiv: ', awayTeamDiv.text, 'homeTeamDiv: ', homeTeamDiv.text)
                        awayTeam = ""
                        homeTeam = ""
                        winningTeam = None
                        losingTeam = None
                        winningScore = None
                        losingScore = None
                        predictionRow = False
                        # print('columns:', len(columns))
                        # for column in columns:
                        #     print('rowIndex:', rowIndex, 'columnIndex:', columnIndex, column.text.find(" at "))
                        #     if rowIndex == 0:
                        #         if columnIndex == 0:
                        #             if column.text.find(" at ") > -1:

                        #                 predictionRow = True
                        #                 teamSpans = column.find_element(By.TAG_NAME, "span")
                        #                 openParenthesis = teamSpans.text.find("(")
                        #                 closeParenthesis = teamSpans.text.find(")")
                        #                 separator = teamSpans.text.find(" at ")
                        #                 awayTeam = ""
                        #                 homeTeam = ""
                        #                 if openParenthesis > separator:
                        #                     awayTeam = teamSpans.text[:separator]
                        #                     homeTeam = teamSpans.text[separator+4:openParenthesis-1]
                        #                 else:
                        #                     awayTeam = teamSpans.text[:openParenthesis-1]
                        #                     homeTeam = teamSpans.text[separator+4:]
                        #                 print(awayTeam, homeTeam)
                        #         else:
                        #             if predictionRow == True:
                        #                 teamImage = column.find_element(By.TAG_NAME, "img")
                        #                 teamImageSrc = teamImage.get_attribute("src")
                        #                 print('teamImageSrc:', imageTable, teamImageSrc)
                        #                 winningTeam = imageTable[teamImageSrc]
                        #                 if winningTeam == awayTeam:
                        #                     losingTeam = homeTeam
                        #                 else:
                        #                     losingTeam = awayTeam
                        #                 print('winningTeam:', winningTeam, 'losingTeam:', losingTeam)
                        #                 author = writersText[columnIndex-1]["name"] 
                        #                 predictions.append({"author": author,"winningTeam": winningTeam, "losingTeam": losingTeam})
                        #         if predictionRow == True and columnIndex == len(columns)-1:
                        #             rowIndex = 1
                        #         columnIndex = columnIndex + 1
                        #     elif rowIndex == 1:
                        #         scoreSeparator = column.text.find("-")
                        #         if scoreSeparator > -1:
                        #             winningScore = column.text[:scoreSeparator].strip()
                        #             losingScore = column.text[scoreSeparator+1:].strip()
                        #             print('winningScore:', winningScore, 'losingScore:', losingScore)
                        #             predictions[columnIndex-1]["winningScore"] = winningScore
                        #             predictions[columnIndex-1]["losingScore"] = losingScore
                        #             print('predictions:', predictions)
                        #             if columnIndex == len(columns)-1:
                        #                 for prediction in predictions:
                        #                     print('author:', prediction["author"], prediction["winningTeam"], prediction["winningScore"], prediction["losingTeam"], prediction["losingScore"])
                        #                     usatodayrows.append([prediction["author"], prediction["winningTeam"], prediction["winningScore"], prediction["losingTeam"], prediction["losingScore"]])
                        #                     predictions = []
                        #                 rowIndex = 0
                        #         columnIndex = columnIndex + 1
                    else:
                        print('parent elements not found', parentElements.text)
            except Exception as e:
                print('Exception:', e)
                traceback.print_exc()
        else:
            pickLinkIndex = 0
            articleBody = driver.find_element(By.TAG_NAME, "article")
            wait.until(lambda d : articleBody.is_displayed())
            pickLinks = articleBody.find_elements(By.XPATH,'//a[contains(text(), " vs. ")]')    # pickLinks2 = driver.find_elements(By.XPATH, "/html/body/div[3]/main/article/div[5]/p[10]/a")
            print('usatoday picklinks 37:', len(pickLinks))
            while pickLinkIndex < len(pickLinks):
                
                popup = driver.find_elements(By.CLASS_NAME, "gnt_mol_xb")
                if len(popup) > 0:
                    popup[0].click()
                pickLinks[pickLinkIndex].click()
                if len(driver.window_handles) > 1:
                    driver.switch_to.window(driver.window_handles[len(driver.window_handles)-1])
                articleBody = driver.find_element(By.TAG_NAME, "article")
                wait.until(lambda d : articleBody.is_displayed())
                title = driver.find_element(By.TAG_NAME, "h1")
                wait.until(lambda d : title.is_displayed())
                headers = driver.find_elements(By.TAG_NAME, "h2")
                headerIndex = 0
                for header in headers:
                    winnerScore = None
                    winningTeam = None
                    losingScore = None
                    losingTeam = None
                    if headerIndex > 1:
                        separatorIndex = header.text.find(":")
                        author = header.text[:separatorIndex].replace(" ","")
                        winner = header.text[separatorIndex+2:header.text.find(",")].split(" ")
                        winningTeam = winner[0]
                        if len(winner) > 1:
                            winningScore = winner[1]
                        loser = header.text[header.text.find(",")+2:].split(" ")
                        losingTeam = loser[0]
                        if len(loser) > 1:
                            losingScore = loser[1]
                        print('author:', author, winningTeam, winningScore, losingTeam, losingScore)
                        usatodayrows.append([author,winningTeam, winningScore, losingTeam, losingScore])                    
                    headerIndex = headerIndex + 1
                pickLinkIndex = pickLinkIndex + 1 
                driver.get(url)
                popup = driver.find_elements(By.CLASS_NAME, "gnt_mol_xb")
                if len(popup) > 0:
                    popup[0].click()
                articleBody = driver.find_element(By.TAG_NAME, "article")
                wait.until(lambda d : articleBody.is_displayed())

                pickLinks = articleBody.find_elements(By.XPATH,'//a[contains(text(), " vs. ")]')
                print('usatoday picklinks 80:', len(pickLinks))
        print('usatodayrows:', usatodayrows)
        return usatodayrows
    except Exception as e:
        print('Exception:', e)
        traceback.print_exc()
        return usatodayrows


def main(weeknum):
    html_content = fetch_usatoday_data(weeknum, 'https://e.infogram.com/d1870792-ebfe-46f3-9734-f9013606d428?src=embed#async_embed') #'https://tallysight.com/new/widget/staff-picks/usa-today-sports/nfl/event:2024-25-week-17/default:ml/types:ml,ats/extras:condensed/performances:bboverall,overall?id=5fef16ef-7f0c-41e5-81c9-a000636d9d0c'
    if html_content:
        print(html_content)
    else:
        print("Failed to retrieve data")

if __name__ == "__main__":
    weeknum = sys.argv[0]
    main(weeknum)
