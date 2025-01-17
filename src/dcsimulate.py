import subprocess
import threading
import json
from dataclasses import dataclass
from copy import deepcopy
from typing import Optional, Any
import time

@dataclass
class ShotParam:
    x: float
    y: float
    rotation: str
    game_state: Optional[dict[str, Any]]

class Simulate:
    def __init__(self, port: int = 10000):
        super(Simulate, self).__init__
        cpp_command = [f"/workspace/DigitalCurling3-ClientExamples/build/stdio/digitalcurling3_client_examples__stdio", "localhost", str(port)]
        self.process = subprocess.Popen(cpp_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE)

        self.first_flag = True

        output = self.process.stdout.readline()
        if output.decode().strip().startswith("inputwait"):
            self.first_flag = True
            game_state = json.loads(output.decode().strip().split()[1])
    
    
    def shot(self, shot_param: ShotParam, preview: bool, process) -> Optional[dict[str, Any]]:
        if preview is False:
            mode = "shot"
        elif shot_param.game_state:
            mode = "simufile"
        else:
            mode = "simu"
        
        if self.first_flag is True:
            cpp_input = f"{shot_param.x} {shot_param.y} {shot_param.rotation} {mode} {json.dumps(shot_param.game_state, separators=(',', ':'))}\n" # 送信する入力データ
            process.stdin.write(cpp_input.encode())
            process.stdin.flush()
        else:
            while True:
                if process.poll() is not None:
                    quit()
                output = process.stdout.readline()
                if output.decode().startswith("inputwait"):
                    cpp_input = f"{shot_param.x} {shot_param.y} {shot_param.rotation} {mode} {json.dumps(shot_param.game_state, separators=(',',':'))}\n" # 送信する入力データ
                    process.stdin.write(cpp_input.encode())
                    process.stdin.flush()
                    break
        if mode != "shot":
            self.first_flag = False
            while True:
                if process.poll() is not None:
                    quit()
                output = process.stdout.readline()
                if output.decode().startswith("jsonoutput"):
                    game_state = json.loads(output.decode().strip().split()[1])
                    return game_state
                if output.decode().strip() in ["won the game", "lost the game"]:
                    quit()
        else:
            return None
    

    def simulate(self, shot_param: ShotParam, process) -> dict[str, Any]:
        game_state = self.shot(shot_param, True, process)
        return game_state


    def __call__(self, x: float, y: float, r: str, game_state: dict[str, Any]) -> dict[str, Any]:
        shot_param = ShotParam(x, y, r, game_state)
        sim_game_state = self.simulate(shot_param, self.process)

        return sim_game_state