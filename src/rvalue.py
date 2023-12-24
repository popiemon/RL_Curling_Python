#! Python3

from typing import Any
import numpy as np
import pandas as pd

class Rvalue:
    """R値を計算
    """
    def __init__(self, team: str, point: str) -> None:
        """R値を計算

        Args:
            team (str): team0 or team1
            point (str): 相手のstoneよりも内側のstone 1個ずつに入る得点
        """
    super(Rvalue, self).__init__
    self.house_cx = 0.0
    self.house_cy = 38.405
    self.house_r = 1.829

    self.point_r = point

    assert ((team == "team0") or (team == "team1")), 'Expected team is team0 or team1, but team is {0}'.format(team)

    if team == "team0":
        self.team = team
        self.enemy = "team1"
    elif team == "team1":
        self.team = team
        self.enemy = "team0"

    def __call__(self, map: pd.DataFrame, omega: float = 0.95) -> float:
        """stones 情報の dataframe からR値を計算

        Args:
            map (pd.DataFrame): stones 情報の dataframe
            omega (float, optional): 重み. Defaults to 0.95.

        Returns:
            float: R値
        """
        rmap = map.fillna(0)

        if rmap.empty: # stoneがすべてNaN
            return 0
        else:
            rmap["distance"] = np.sqrt((rmap["x"]-self.house_cx)**2 + (rmap["y"]-self.house_cy)**2)
            rmap["house-distance"] = self.house_r - rmap["distance"]
            rmap['R'] = 0

            t0_df = rmap[rmap["team"] == "team0"]
            t1_df = rmap[rmap["team"] == "team1"]
            t0_dis = t0_df["distance"].values
            t1_dis = t1_df["distance"].values

            th_dis = max(np.min(t0_dis), np.min(t1_dis)) # team0, team1 の最も中心に近いstone の距離の大きい方

            rmap.loc[rmap['distance'] < th_dis, 'R'] = self.point_r # 相手のstoneよりも内側のstoneに得点
            rmap['Rtot'] = rmap["house-distance"] + rmap['R']

            team_df = rmap.groupby("team").get_group(self.team)
            enem_df = rmap.groupby("team").get_group(self.enemy)

            return omega*team_df["Rtot"].sum() - (1-omega)*enem_df["Rtot"].sum()

