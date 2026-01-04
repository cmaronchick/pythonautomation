import pandas as pd
import csv, json, os, ast, sys

    #"ID": "duos",
    #   "NameID": "UI_ABILITY_DUOS",
    #   "IconPath": "data/cards/frames/textures/ability_icons/ability_01.tga",
    #   "AbilityType": 0,
    #   "DataTypeNum1": 20051,
    #   "DataTypeNum2": -1,
    #   "DataTypeNum3": -1,
    #   "ActionType": 0,
    #   "ActionDataTypeFloat": 1.2

def iterateObject(object):
    datarow = []
    for key, value in object.items():
        datarow.append(value)
    return datarow

def iterateFile(full_path, file, game):
    
    filename = os.fsdecode(full_path)
    shortname = os.path.basename(filename)
    with open(filename, encoding='utf-8') as inputfile:
        df = json.load(inputfile)
        
        headerrow = []
        try: 
            with open(full_path, 'r', encoding='utf-8') as jfile:
                # jsonFile = json.load(jfile)
                content = json.load(jfile)
                # jContent = json.dumps(jfile)

                if hasattr(content,"items"):
                    for key, value in content.items():
                        # print(f"Key: {key}, Value: {value}")
                        if isinstance(value, list): 
                            print('array found', file, key)
                            
                            # filename = key
                            f = csv.writer(open('./' + str(game) + '/' + str(shortname) + '_' + str(key) + ".csv", 'w+', newline='', encoding='utf-8'))
                            for obj in value:
                                print('isinstance(obj, list):', isinstance(obj, list), ', isinstance(obj, dict):', isinstance(obj, dict), len(obj))
                                datarow = []
                                if (isinstance(obj, list) or isinstance(obj, dict)) and len(obj) > 0: 
                                    if len(headerrow) == 0:
                                        for key, value in obj.items():
                                            headerrow.append(key)
                                        f.writerow(headerrow)
                                    # print(headerrow)
                                    for key, value in obj.items():
                                        if (isinstance(value, list) or isinstance(value, dict)) and len(value) > 0: 
                                            datarow = iterateObject(value)
                                    f.writerow(datarow)
                                else:
                                    print('key: ', key, 'word: ', value)
                                    # jsonlist = list(word)
                                    # if len(jsonlist) > 0:
                                    f.writerow([key, value])

                else:
                    print('no items df: ', content)
                    f = csv.writer(open('./' + str(game) + '/' + str(shortname) + ".csv", 'w+', newline='', encoding='utf-8'))
                    # lines_dict=ast.literal_eval(jfile.read())
                    # print('lines_dict: ', lines_dict)
                    # for page, word in lines_dict.items():
                    #     print('page, word: ', page, word)
                    # f.writerow(['content'])
                    # f.writerow([content])
                    # Write the header (keys of the first dictionary)
                    if isinstance(content, list) and len(content) > 0:
                        f.writerow(content[0].keys())

                        # Write the rows (values of each dictionary)
                        for entry in content:
                            f.writerow(entry.values())
                    else:
                        print("JSON content is not in the expected list format.")
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print('df: ', file, e, exc_type, fname, exc_tb.tb_lineno)
            try: 
                # print('no items df: ', content)
                with open(full_path, 'r', encoding='utf-8') as jfile:
                    f = csv.writer(open('./' + str(game) + '/' + str(shortname) + ".csv", 'w+', newline='', encoding='utf-8'))
                    lines_dict=ast.literal_eval(str(json.load(jfile)))
                    # print('lines_dict: ', lines_dict)
                    for page, word in lines_dict.items():
                        print('word type: ', type(word))
                        if (isinstance(word, list) or isinstance(word, dict)) and len(word) > 0: 
                            print('word array found', file, page)
                            
                            # filename = key
                            f = csv.writer(open('./' + str(game) + '/' + str(shortname) + '_' + str(page) + ".csv", 'w+', newline='', encoding='utf-8'))
                            for obj in word:
                                # print(obj)
                                datarow = []
                                print('obj type: ', type(obj))
                                if (isinstance(obj, list) or isinstance(obj, dict)) and len(obj) > 0:
                                    if len(headerrow) == 0:
                                        for key, value in obj.items():
                                            headerrow.append(key)
                                        f.writerow(headerrow)
                                    # print(headerrow)
                                    for key, value in obj.items():
                                        datarow.append(value)
                                    f.writerow(datarow)
                                else:
                                    f.writerow([page, obj])
                        else:
                            print('page: ', page, 'word: ', word)
                            # jsonlist = list(word)
                            # if len(jsonlist) > 0:
                            f.writerow([page, word])
                        # print('page:', page, 'word: ', word)
                    # f.writerow(['content'])
                    # f.writerow([content])
                    
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print('df:', file, e, exc_type, fname, exc_tb.tb_lineno)

def iterateDirectory(full_path):
    for file in os.listdir(full_path): 
        if os.path.isfile(full_path):
            print(f"{file, full_path} is a file.")
        elif os.path.isdir(full_path):
            print(f"{file, full_path} is a folder.")
        try: 
            if os.path.isfile(full_path):
                iterateFile(full_path)            
        except Exception as e:
            print('e: ', file, e)

game = "Splash20"
if (len(sys.argv) > 0):
    game = sys.argv[1]
    print('game: ', game)

directory = os.fsencode('C:\\work\\' + str(game) + '\\BobcatData\\LootDefs\\')
for file in os.listdir(directory): 
    full_path = os.path.join(directory, file)
    if os.path.isfile(full_path):
        print(f"{file, full_path} is a file.")
    elif os.path.isdir(full_path):
        print(f"{file, full_path} is a folder.")
    try:
        if os.path.isdir(full_path):
            iterateDirectory(full_path) 
        if os.path.isfile(full_path):
            iterateFile(full_path, file, game)

    # data = json.load('C:\\work\\Splash20\\BobcatData\\CardAbilitySettings.json')
    # with open('C:\\work\\Splash20\\BobcatData\\CardAbilitySettings.json', encoding='utf-8') as inputfile:

    # Iterate through keys and values using .items() method
        # for key, value in data.items():
        #     print(f"Key: {key}, Value: {value}")

        # df.to_csv('abilities.csv', encoding='utf-8', index=False)

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        print('e: ', file, e)