import requests, csv, traceback
adids = open('./wwe_impact_installs.csv',newline='')

rows = []
with adids as csvfile:
    csvreader = csv.reader(adids,delimiter=",")
    for row in csvreader:
        try: 
            if row[0] != 'inst_time':
                adid = row[10]
                response = requests.get('https://api.adjust.com/device_service/api/v2/inspect_device?advertising_id=' + adid + '&app_token=cq2wyunmfl5f', headers={'Authorization': 'Bearer 2tuES44W1hG1oRx8tdxB'})
                # print('response:', response.json())
                events = response.json()
                print('events: ', events)
                if "LastEventsInfo" in response.json():
                    rows.append([events["Adid"], len(events["LastEventsInfo"])])
                else:
                    adid = 'NA'
                    if "Adid" in events:
                        adid = events["Adid"]
                    rows.append([adid, 0])
                    print('no events')
        except ValueError:
            print(traceback.print_exc())


    adidsresponses = open("adids-responses.csv", 'w+', newline='')
    with adidsresponses as csvfile:
        fields = ['adids', 'Events Numbers', 'InstallTime', 'InstallBeginTime']
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields) 
        csvwriter.writerows(rows) 


 
        

