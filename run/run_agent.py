#!Python3

import argparse
import datetime
import yaml

from src.agent import agent

def main():
    with open("config/config.yml", 'r') as yml:
        cfg = yaml.safe_load(yml)
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--dir_name', default=cfg["model"]["name"], help='save dir name.')
    parser.add_argument('--phase', default="train", help='train or test.')
    parser.add_argument('--port', default=10000, help='team0:10000, team1:10001')
    args = parser.parse_args()
    dir_name = str(args.dir_name)
    phase = str(args.phase)
    port = str(args.port)

    agent.run(port = port, dir_name = dir_name, phase = phase)


if __name__ == "__main__":
    main()