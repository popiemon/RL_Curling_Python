import json
import pathlib

from dc3client import SocketClient
from dc3client.models import StoneRotation

import src.data_df as data_df
import src.save_info as save_info

class agent:
    def __init__(self, team: str = "team0", rate_limit: float = 0.5, dir_name: str = None):
        assert (team == "team0") or (team == "team1"), 'Expected team0 or team1, input team is {0}'.format(team)
        
        self.team = team
        self.rate_limit = rate_limit
        self.dir_name = dir_name

    def play(self):
        assert (self.team == "team0") or (self.team == "team1"), 'Expected team0 or team1, input team is {0}'.format(self.team)

        if self.team == "team0":
            port_no = 10000
        elif self.team == "team1":
            port_no = 10001

        cli = SocketClient(host="localhost", port=port_no, client_name="SAMPLE_AI0", auto_start=True, rate_limit=self.rate_limit)

        # ログを出力するディレクトリを指定します。デフォルトでは"logs/"となっています。
        log_dir = pathlib.Path("logs")

        remove_trajectory = True

        # 自分がteam0かteam1かを取得します
        my_team = cli.get_my_team()
        cli.logger.info(f"my_team :{my_team}")

        # dcやis_readyをdataclass形式で取得し、保存しやすいようにdict形式に変換します。
        dc = cli.get_dc()
        dc_message = cli.convert_dc(dc)
        is_ready = cli.get_is_ready()
        is_ready_message = cli.convert_is_ready(is_ready)

        info_df_list = []
        shot_list = []
        shot_rotateion_dict = {0:StoneRotation.clockwise, 1:StoneRotation.inturn, 2:StoneRotation.counterclockwise, 3:StoneRotation.outturn}
        shot = 0

        # 試合を開始します
        while True:

            # updateを受け取ります
            cli.update()

            # 試合状況を取得します
            # 現在の情報は、match_data.update_listに順番に格納されています
            match_data = cli.get_match_data()

            # winnerが存在するかどうかで、試合が終了しているかどうかを確認します
            if (winner := cli.get_winner()) is not None:
                # game end
                if my_team == winner:
                    # 勝利
                    cli.logger.info("WIN")
                else:
                    # 敗北
                    cli.logger.info("LOSE")
                # 試合が終了したらループを抜けます
                break

            # 次のチームが自分のチームかどうかを確認します
            next_team = cli.get_next_team()

            # 次のチームが自分のチームであれば、moveを送信します
            if my_team == next_team:

                ### いろいろ追加 #################################################################
                for update in match_data.update_list:
                    update_dict = cli.convert_update(update, remove_trajectory)
                
                info_df_list.append(data_df.stones(update_dict))
                shot = update_dict["state"]["shot"]

                ## Brain ##
                shot_x = 0.0
                shot_y = 2.4
                shot_rotation = 1

                shot_list.append({"x":shot_x, "y":shot_y, "rotation":shot_rotation})
                ##################################################################################
                
                cli.move(x=shot_x, y=shot_y, rotation=shot_rotateion_dict[shot_rotation])

                ################################# 15shotの結果######################################
                if shot == 15:
                    match_data = cli.get_match_data()
                    for update in match_data.update_list:
                        update_dict = cli.convert_update(update, remove_trajectory)
                    last_shot = update_dict.copy()
                    last_shot["state"]["shot"] = shot+1
                    info_df_list.append(data_df.stones(last_shot))
                ####################################################################################

            else:
                # 次のチームが自分のチームでなければ、何もしません
                continue

        # 試合が終了したら、clientから試合データを取得します
        move_info = cli.get_move_info()
        update_list, trajectory_list = cli.get_update_and_trajectory(remove_trajectory)

        # 試合データを保存します、
        update_dict = {}

        for update in update_list:
            # updateをdict形式に変換します
            update_dict = cli.convert_update(update, remove_trajectory)

        # updateを保存します、どのように保存するかは任意です
        with open("data.json", "w", encoding="UTF-8") as f:
            json.dump(update_dict, f, indent=4)
        
        save_info.list_pickle(info_df_list, self.team, "gamedata/"+self.dir_name, "map")
        save_info.list_pickle(shot_list, self.team, "gamedata/"+self.dir_name, "shot")

