# import pandas as pd
import json, csv, datetime

today = datetime.date.today()
with open('playcard-' + str(today) + '.csv', 'a', newline='') as csvfile:
    fieldNames = ["ID", "Phase Type", "Play Name", "Play Type", "Quality"]
    # gcwriter = csv.DictWriter(csvfile, fieldnames=fieldNames) #, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL
    # gcwriter.writeheader()
    rows = []
    with open("C:/work/Phoenix/bobcatsettingshistory/qa/Game/PlayCardDefinitions_Season1.json", "r") as read_file:
        playcardsfile = json.load(read_file)
        playcards = playcardsfile["PlayCardList"]
        for playcard in playcards:
            ID = playcard["ID"]
            phaseType = playcard["PhaseType"]
            playName = playcard["Name"]
            playType = playcard["PlayType"]
            playQuality = playcard["Quality"]
            rows.append({"ID": ID, "Phase Type": phaseType, "Play Name": playName, "Play Type": playType, "Quality": playQuality})
            
        # gcwriter.writerow({'Week': week, 'Week Type': weekType, "Start": start, "End": end})
        playcardswriter = csv.DictWriter(csvfile, fieldnames=fieldNames) #, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL
        playcardswriter.writeheader()
        playcardswriter.writerows(rows)
                    
        # print(week,"\n",
        # weekType,"\n",
        # start,"\n",
        # end)


    
# .to_excel("output.xlsx")