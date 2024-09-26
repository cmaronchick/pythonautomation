from pymongo import MongoClient, UpdateOne
import csv
from datetime import date

weeknum = 3

predictions = open("2024week" + str(weeknum) + "picks.csv",newline='')

client = MongoClient("mongodb+srv://pcsm-user:*dZ2HaWN@pcsm.lwx4u.mongodb.net/pcsm?retryWrites=true&w=majority")
db = client['pcsm']
collection = db['games']
predictionsCollection = db['predictions']

games = list(collection.find({ "sport": 'nfl', "season": "reg", "year": 2024, "gameWeek": weeknum}))
print(len(games))
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
        print('row:', row)
        if row[0] != "Source":
            awayCode = row[6]
            homeCode = row[7]
            awayScore = int(row[8])
            homeScore = int(row[9])
            gameObj = {
                "year": 2024,
                "sport": "nfl",
                "season": "reg",
                "gameWeek": weeknum,
                "awayTeam": {
                    "code": awayCode,
                    "score": awayScore
                },
                "homeTeam": {
                    "code": homeCode,
                    "score": homeScore
                },
                "userId": row[0],
                "preferred_username": row[0],
                "submitted": date.isoformat(date.today()),
                "spread": homeScore - awayScore,
                "total": homeScore + awayScore
            }
            print('games:', len(games))
            gameId = None
            for game in games:
                print('game:', game["awayTeam"]["code"], game["homeTeam"]["code"], awayCode, homeCode)
                if awayCode == game["awayTeam"]["code"] is True or homeCode == game["homeTeam"]["code"]:
                    gameObj["gameId"] = game["gameId"]
                    gameObj["odds"] = {
                        "spread": game["odds"]["spread"],
                        "total": game["odds"]["total"]
                    }
            
            # print("gameObj: ", gameObj)
            if "gameId" in gameObj:
                updates.append(UpdateOne({
                "year": 2024,
                "sport": "nfl",
                "season": "reg",
                "gameWeek": weeknum,
                "userId": row[0],
                "gameId": gameObj["gameId"]
                }, {"$set": gameObj}, upsert=True))
    print('updates:', len(updates))
    predictionsUpdateResponse = predictionsCollection.bulk_write(updates)
    print('predictionsUpdateResponse: ', predictionsUpdateResponse.bulk_api_result)

        # print('awayCode, homeCode:', awayCode, homeCode)
        # filteredGame = list(filter(lambda game: awayCode == game["awayTeam"]["code"] is True or homeCode == game["homeTeam"]["code"] is True, games))
        # print('len', len(filteredGame))
        # for fg in filteredGame:
        #     print('filteredGame:', fg)


