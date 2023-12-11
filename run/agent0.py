#!Python3

import argparse
import datetime

from src.agent import agent

if __name__ == "__main__":
    now = datetime.datetime.now()
    ydh = now.strftime('%Y%m%d%H%M')

    parser = argparse.ArgumentParser()
    parser.add_argument('--dir_name', default=ydh, help='save dir name.')
    args = parser.parse_args()
    dir_name = str(args.dir_name)

    agent0 = agent(team = "team0", dir_name=dir_name, rate_limit=0.1)
    agent0.play()