#! Python3

import os
import pickle
import datetime

def list_pickle(info_list: list, team: str, savedir: str = 'data', fname: str = None) -> None:
    os.makedirs(savedir, exist_ok=True)
    fname = savedir + "/" + fname + "_" + team + ".pickle"

    with open(fname, mode='wb') as fo:
        pickle.dump(info_list, fo)