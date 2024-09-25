from pymongo import MongoClient, UpdateOne
import csv
from datetime import date

weeknum = 3

predictions = open("2024week" + str(weeknum) + "picks.csv",newline='')

client = MongoClient("mongodb+srv://pcsm-user:*dZ2HaWN@pcsm.lwx4u.mongodb.net/pcsm?retryWrites=true&w=majority")
db = client['pcsm']
collection = db['games']
predictionsCollection = db['predictions']

games = collection.find({ "sport": 'nfl', "season": "reg", "year": 2024, "gameWeek": weeknum})

def filterGames(awayCode,homeCode):
    for game in games:
        if awayCode == game["awayTeam"]["code"] is True or homeCode == game["homeTeam"]["code"] is True:
            return True
        else:
            return False
updates = []
with predictions as csvfile:
    csvreader = csv.reader(predictions,delimiter=",")
    for row in csvreader:
        if row[0] != "Source":
            awayScore = int(row[8])
            homeScore = int(row[9])
            gameObj = {
                "year": 2024,
                "sport": "nfl",
                "season": "reg",
                "gameWeek": weeknum,
                "awayTeam": {
                    "code": row[6],
                    "score": awayScore
                },
                "homeTeam": {
                    "code": row[7],
                    "score": homeScore
                },
                "userId": row[0],
                "preferred_username": row[0],
                "submitted": date.isoformat(date.today()),
                "spread": homeScore - awayScore,
                "total": homeScore + awayScore
            }
            gameId = None
            for game in games:
                if gameObj["awayTeam"]["code"] == game["awayTeam"]["code"] is True or gameObj["homeTeam"]["code"] == game["homeTeam"]["code"]:
                    gameObj["gameId"] = game["gameId"]
                    gameObj["odds"] = {
                        "spread": game["odds"]["spread"],
                        "total": game["odds"]["total"]
                    }
            
            # print("gameObj: ", gameObj)
            updates.append(UpdateOne({
            "year": 2024,
            "sport": "nfl",
            "season": "reg",
            "gameWeek": weeknum,
            "userId": row[0]
            }, {"$set": gameObj}, upsert=True))
    print('updates:', len(updates))
    predictionsUpdateResponse = predictionsCollection.bulk_write(updates)
    print('predictionsUpdateResponse: ', predictionsUpdateResponse)

        # print('awayCode, homeCode:', awayCode, homeCode)
        # filteredGame = list(filter(lambda game: awayCode == game["awayTeam"]["code"] is True or homeCode == game["homeTeam"]["code"] is True, games))
        # print('len', len(filteredGame))
        # for fg in filteredGame:
        #     print('filteredGame:', fg)


