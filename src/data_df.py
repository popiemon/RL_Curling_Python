#! Python3

import pandas as pd
import numpy as np

def stones(update: dict) -> pd.DataFrame:
    """盤面情報のdictから stones の dataframe を作成

    Args:
        update (dict): 盤面情報の state dict

    Returns:
        pd.DataFrame: stones の angle, x, y が記述されたdataframe
    """
    datalist = []
    stone_dict = update["stones"]
    shot = update["shot"]
    end = update["end"]
    for k in stone_dict.keys():
        team = k
        info_flag = 0
        for info in stone_dict[k]:
            if info is not None:
                info_flag = 1 # 最低1つstone情報があるとき
                angle = info["angle"]
                x = info["position"]["x"]
                y = info["position"]["y"]
                datalist.append([end, team, shot, angle, x, y])
        if info_flag == 0: # 1つもstoneの情報がなかったとき
            datalist.append([end, team, shot, np.nan, np.nan, np.nan])

        df = pd.DataFrame(datalist, columns=['end', 'team', 'shot', 'angle', 'x', 'y'])
        return df