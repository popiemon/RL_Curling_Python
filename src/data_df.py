#! Python3

import pandas as pd

def stones(update: dict) -> pd.DataFrame:
    datalist = []
    for k in update.keys():
        team = k
        for info in update[k]:
            angle = info["angle"]
            x = info["position"]["x"]
            y = info["position"]["y"]
            datalist.append([team, angle, x, y])
        
    df = pd.DataFrame(datalist, columns=['team', 'angle', 'x', 'y'])
    return df