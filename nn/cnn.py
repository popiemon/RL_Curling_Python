#! Python3

import torch
import torch.nn as nn

class CNN(nn.Module):
    def __init__(self, dim):
        super(CNN, self).__init__()

        self.conv1 = nn.Conv2d(1, 16, kernel_size=3, stride=1, padding=1)
        self.elu1 = nn.ELU()
        self.maxpool1 = nn.MaxPool2d(kernel_size=2, stride=2)

        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, stride=1, padding=1)
        self.elu2 = nn.ELU()
        self.maxpool2 = nn.MaxPool2d(kernel_size=2, stride=2)

        self.conv3 = nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1)
        self.elu3 = nn.ELU()
        self.maxpool3 = nn.MaxPool2d(kernel_size=2, stride=2)

        self.fc1 = nn.Linear(64 * 8 * 8, 128)
        self.elu4 = nn.ELU()

        self.fc2 = nn.Linear(128, dim)

    def forward(self, x):
        x = self.conv1(x)
        x = self.elu1(x)
        x = self.maxpool1(x)

        x = self.conv2(x)
        x = self.elu2(x)
        x = self.maxpool2(x)

        x = self.conv3(x)
        x = self.elu3(x)
        x = self.maxpool3(x)

        x = x.view(x.size(0), -1)

        x = self.fc1(x)
        x = self.elu4(x)

        output = self.fc2(x)

        return output


