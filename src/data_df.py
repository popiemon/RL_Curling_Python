#! Python3

import pandas as pd

def stones(update: dict) -> pd.DataFrame:
    datalist = []
    stone_dict = update["state"]["stones"]
    shot = update["state"]["shot"]
    end = update["state"]["end"] 
    for k in stone_dict.keys():
        team = k
        for info in stone_dict[k]:
            angle = info["angle"]
            x = info["position"]["x"]
            y = info["position"]["y"]
            datalist.append([end, team, shot, angle, x, y])
        
    df = pd.DataFrame(datalist, columns=['end', 'team', 'shot','angle', 'x', 'y'])
    return df

def log_stones(update: dict) -> pd.DataFrame:
    datalist = []
    stone_dict = update["log"]["trajectory"]["finish"]
    shot = update["log"]["shot"]
    end = update["log"]["end"]
    for k in stone_dict.keys():
        team = k
        for info in stone_dict[k][0]:
            angle = info["angle"]
            x = info["position"]["x"]
            y = info["position"]["y"]
            datalist.append([end, team, shot, angle, x, y])
        
    df = pd.DataFrame(datalist, columns=['end', 'team', 'shot','angle', 'x', 'y'])
    return df
