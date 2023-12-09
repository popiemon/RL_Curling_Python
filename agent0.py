#!Python3

from src.agent import agent

if __name__ == "__main__":
    agent0 = agent(team = "team0", rate_limit=0.1)
    agent0.play()