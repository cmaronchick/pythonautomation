from pymongo import MongoClient, UpdateOne
import csv, boto3, sys
from datetime import date, datetime

sns = boto3.client('sns', region_name='us-west-2')

weeknum = 13
if (len(sys.argv) > 1):
    weeknum = int(sys.argv[1])
print('weeknum:', weeknum)
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
updateGameIds = []
with predictions as csvfile:
    csvreader = csv.reader(predictions,delimiter=",")
    for row in csvreader:
        print('row:', row)
        if row[0] != "Source":
            awayCode = row[6]
            awayShortName = row[7]
            awayFullName = row[8]
            homeCode = row[9]
            homeShortName = row[10]
            homeFullName = row[11]
            awayScore = int(row[12])
            homeScore = int(row[13])
            gameObj = {
                "year": 2024,
                "sport": "nfl",
                "season": "reg",
                "gameWeek": weeknum,
                "awayTeam": {
                    "code": awayCode,
                    "shortName": awayShortName,
                    "fullName": awayFullName,
                    "score": awayScore
                },
                "homeTeam": {
                    "code": homeCode,
                    "shortName": homeShortName,
                    "fullName": homeFullName,
                    "score": homeScore
                },
                "userId": row[0],
                "preferred_username": row[0],
                "submitted": datetime.strptime(str(datetime.now().year) + "-" + str(datetime.now().month) + "-" + str(datetime.now().day) + "T" + str(datetime.now().hour) + ":" + str(datetime.now().minute) + ":" + str(datetime.now().second), '%Y-%m-%dT%H:%M:%S'),
                "spread": awayScore - homeScore,
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
                updateGameIds.append({"gameId": gameObj["gameId"], "gameWeek": weeknum, "sport": "nfl", "season": "reg", "year": 2024})
    print('updates:', len(updates))
    predictionsUpdateResponse = predictionsCollection.bulk_write(updates)
    print('predictionsUpdateResponse: ', predictionsUpdateResponse) # len(predictionsUpdateResponse.bulk_api_result["modifiedCount"])
    # for update in updateGameIds:
    #     sns.publish(
    #         TopicArn="arn:aws:sns:us-west-2:198282214908:predictionSubmitted",
    #         Message="Prediction for game " + str(update["gameId"]), 
    #         Subject="Prediction Submitted" + str(update["gameId"]),
    #         MessageAttributes={ 
    #             "gameId": {
    #                 "DataType": "Number",
    #                 "StringValue": str(update["gameId"])
    #             },
    #             "gameWeek": {
    #                 "DataType": "Number",
    #                 "StringValue": str(update["gameWeek"])
    #             },
    #             "year": {
    #                 "DataType": "Number",
    #                 "StringValue": str(update["year"])
    #             },
    #             "sport": {
    #                 "DataType": "String",
    #                 "StringValue": update["sport"]
    #             },
    #             "season": {
    #                 "DataType": "String",
    #                 "StringValue": update["season"]
    #             }
    #         })

        # print('awayCode, homeCode:', awayCode, homeCode)
        # filteredGame = list(filter(lambda game: awayCode == game["awayTeam"]["code"] is True or homeCode == game["homeTeam"]["code"] is True, games))
        # print('len', len(filteredGame))
        # for fg in filteredGame:
        #     print('filteredGame:', fg)


