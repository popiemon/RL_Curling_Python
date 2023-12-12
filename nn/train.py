#! Python3

import numpy as np
import torch
import torch.nn as nn

from nn.cnn import CNN

class Training:
    def __init__(self) -> None:
        super(Training, self).__init__()
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'

        model = CNN()
        self.model = model.to(self.device)
        self.criterion = nn.MSELoss()
        self.optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    
    def training(self, output: np.array, label: np.array) -> None:
        