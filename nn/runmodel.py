#! Python3

import os
import numpy as np
import torch
import torch.nn as nn

from nn.cnn import CNN

class DQN:
    """Neural Network Training Class"""
    def __init__(self, dim: int, model_path: str = None, modelname: str = None) -> None:
        """Initialize Training Class"""
        super(DQN, self).__init__()
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'

        model = CNN(dim)
        modelfile = model_path + '/' + modelname
        if os.path.isfile(modelfile):
            print(modelfile, "model is loaded.")
            model.load_state_dict(torch.load(modelfile))

        self.model = model.to(self.device)
        self.criterion = nn.MSELoss()
        self.optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

    
    def training(self, map: np.array, qtp1: np.array, rtp1: np.array) -> None:
        """DQN

        Args:
            map (np.array): stoneのmap s(t)
            qtp1 (np.array): Q(t+1)
            rtp1 (np.array): R(t+1)
        """

        self.model.train()

        input = torch.tensor(map, dtype=torch.float32)
        input = input.unsqueeze(0).unsqueeze(0)
        input = input.to(self.device)
        output = self.model(input)

        label = rtp1 + qtp1
        label = torch.tensor(label, dtype=torch.float32)
        label = label.unsqueeze(0)
        label = label.to(self.device)

        self.optimizer.zero_grad()

        loss = self.criterion(output, label)
        loss.backward()
        self.optimizer.step()

    
    def predict(self, input: np.array) -> np.array:
        """推論

        Args:
            input (np.array): 2D stone map

        Returns:
            np.array: stone のパラメータ a(t)
        """
        self.model.eval()

        with torch.no_grad():
            input = torch.tensor(input, dtype=torch.float32)
            input = input.unsqueeze(0).unsqueeze(0)
            input = input.to(self.device)
            output = self.model(input)

        return output.to('cpu').detach().numpy().copy()
    

    def save_model(self, dir_path: str, modelname: str) -> None:
        """model の保存

        Args:
            dir_path (str): model 保存 dir
            modelname (str): 保存する model の名前
        """
        torch.save(self.model.state_dict(), dir_path + '/' + modelname)
        print("model is saved.", dir_path + '/' + modelname)
        