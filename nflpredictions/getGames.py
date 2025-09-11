from pymongo import MongoClient, UpdateOne
import csv, boto3, sys, traceback
from datetime import date, datetime

sns = boto3.client('sns', region_name='us-west-2')
teams = open("teams.csv", 'r')
weeknum = 1
year = 2024
season = "reg"
if (len(sys.argv) > 3):
    weeknum = int(sys.argv[1])
    year = int(sys.argv[2])
    season = sys.argv[3]
    print('weeknum:', weeknum)

    client = MongoClient("mongodb+srv://pcsm-user:*dZ2HaWN@pcsm.lwx4u.mongodb.net/pcsm?retryWrites=true&w=majority")
    db = client['pcsm']
    collection = db['games']

    games = list(collection.find({ "sport": 'nfl', "season": season, "year": year, "gameWeek": weeknum}))
    rows = []
    try:
        for game in games:
            print('game: ', game)
            print('awayTeam:', game["awayTeam"]["code"])
            print('homeTeam:', game["homeTeam"]["code"])
            rows.append([game["awayTeam"]["shortName"], game["awayTeam"]["code"] + game["homeTeam"]["code"], game["awayTeam"]["code"], game["homeTeam"]["code"], game["gameId"], game["odds"]["spread"], game["odds"]["total"]])
            if (game["awayTeam"]["code"] == "TB"):
                rows.append(["Bucs", game["awayTeam"]["code"] + game["homeTeam"]["code"], game["awayTeam"]["code"], game["homeTeam"]["code"], game["gameId"], game["odds"]["spread"], game["odds"]["total"]])
            if (game["awayTeam"]["code"] == "NE"):
                rows.append(["Pats", game["awayTeam"]["code"] + game["homeTeam"]["code"], game["awayTeam"]["code"], game["homeTeam"]["code"], game["gameId"], game["odds"]["spread"], game["odds"]["total"]])
            rows.append([game["homeTeam"]["shortName"], game["awayTeam"]["code"] + game["homeTeam"]["code"], game["awayTeam"]["code"], game["homeTeam"]["code"], game["gameId"], game["odds"]["spread"], game["odds"]["total"]])
            if (game["homeTeam"]["code"] == "TB"):
                rows.append(["Bucs", game["awayTeam"]["code"] + game["homeTeam"]["code"], game["awayTeam"]["code"], game["homeTeam"]["code"], game["gameId"], game["odds"]["spread"], game["odds"]["total"]])
            if (game["homeTeam"]["code"] == "NE"):
                rows.append(["Pats", game["awayTeam"]["code"] + game["homeTeam"]["code"], game["awayTeam"]["code"], game["homeTeam"]["code"], game["gameId"], game["odds"]["spread"], game["odds"]["total"]])
        week1picks = open(str(year) + str(season) + "week" + str(weeknum) + "games.csv", 'w+', newline='')
        with week1picks as csvfile:
            
            # creating a csv writer object  
            csvwriter = csv.writer(csvfile)  
                
            # writing the fields  
            
            fields = ['SHORT NAME', 'GAMEID', 'AWAY', 'HOME']
            csvwriter.writerow(fields)  
                
            # writing the data rows  
            csvwriter.writerows(rows) 
    except Exception as e:
        print('Exception:', e)
        traceback.print_exc()
        print('Failed to retrieve data')
else:
    print("you must add weeknum, year, and season")
    
