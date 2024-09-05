# import pandas as pd
import json, csv, datetime

today = datetime.date.today()
with open('gc-' + str(today) + '.csv', 'a') as csvfile:
    fieldNames = ["Week","Week Type", "Start", "End"]
    # gcwriter = csv.DictWriter(csvfile, fieldnames=fieldNames) #, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL
    # gcwriter.writeheader()
    rows = []
    with open("C:/work/Phoenix/bobcatsettingshistory/qa/Game/PlaymakersSettings.json", "r") as read_file:
        gcsettings = json.load(read_file)
        weeklyschedule = gcsettings["WeeklySchedule"]
        for weekObj in weeklyschedule:
            week = weekObj["Week"]
            weekType = weekObj["WeekType"]
            schedule = weekObj["Schedule"]
            start = schedule["Start"]
            end = schedule["End"]
            
            # gcwriter.writerow({'Week': week, 'Week Type': weekType, "Start": start, "End": end})
            games = weekObj["Games"]
            gameFieldNames = ["Week","Week Type", "Start", "End", "GameId", "Game Type", "QuestionId", "Question","Question Type", "Type", "StatId", "Info", "Value"]
            gcgameswriter = csv.DictWriter(csvfile, fieldnames=gameFieldNames) #, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL
            gcgameswriter.writeheader()
            gameId = 0
            for game in games:
                gameType = game["Type"]
                # awayTeam = game["Matchups"]["AwayTeam"]
                # homeTeam = game["Matchups"]["HomeTeam"]
                questions = game["Questions"]
                questionId = 0
                for questionObj in questions:
                    questionType = questionObj["QuestionType"]
                    question = questionObj["Question"]
                    swapType = ""
                    statId = ""
                    swapInfo = ""
                    swapValue = ""
                    if "QuestionCypher" in questionObj:
                        questionCypher = questionObj["QuestionCypher"]
                        swapType = questionCypher["Type"]
                        if "StatIds" in questionCypher:
                            statId = questionCypher["StatIds"]
                        if "Info" in questionCypher:
                            swapInfo = questionCypher["Info"]
                        if "Value" in questionCypher:
                            swapValue = questionCypher["Value"]
                    rows.append({"Week": week, "Week Type": weekType, "Start": start, "End": end, "GameId": gameId, "Game Type": gameType, "QuestionId": questionId, "Question": question, "Question Type": questionType, "Type": swapType, "StatId": statId, "Info": swapInfo, "Value": swapValue})
                    questionId += 1
                gameId += 1
            gcgameswriter.writerows(rows)
                    
            print(week,"\n",
            weekType,"\n",
            start,"\n",
            end)


    
# .to_excel("output.xlsx")