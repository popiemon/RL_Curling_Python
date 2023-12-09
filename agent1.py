#!Python3

from src.agent import agent

if __name__ == "__main__":
    agent1 = agent(team = "team1", rate_limit=0.1)
    agent1.play()