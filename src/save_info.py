#! Python3

import pickle
import datetime

def list_pickle(info_list: list, team: str, savedir: str = 'data') -> None:
    now = datetime.datetime.now()
    ydh = now.strftime('%Y%m%d%H%M')
    fname = savedir + "/" + team + "_" + str(ydh) + ".pickle"

    with open(fname, mode='wb') as fo:
        pickle.dump(info_list, fo)