#!usr/bin/env python
# -*- coding: utf-8 -*-
# Script:       model.py
# Description:  prepare network-model
# Update date:  2020/1/2(unfinished)
# Author:       Zhuofan Zhang
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from collections import OrderedDict

#####     Model demo    #####
# class LeNet(nn.Module):
#     def __init__(self, input_len, ngpu=0):
#         super(LeNet, self).__init__
#         self.ngpu = ngpu
#         self.input_len = input_len

#         self._lenet5 = nn.Sequential(OrderedDict([
#             ('conv1', nn.Conv2d(1, 6, 5)),
#             ('relu1', nn.ReLU()),
#             ('pool1', nn.MaxPool2d(2, 2)),
#             ('conv2', nn.Conv2d(6, 16, 5)),
#             ('relu2', nn.ReLU()),
#             ('pool2', nn.MaxPool2d(2, 2)),
#             ('fc1'  , nn.Linear(16*5*5, 120)),
#             ('relu3', nn.ReLU())
#             ('fc2'  , nn.Linear(120, 84)),
#             ('relu4', nn.ReLU())
#             ('fc3'  , nn.Linear(84, 10))
#         ]))

#     def forward(self, x):
#         output = nn.Linear(self.input_len, 32*32)(x)
#         output = output.view(32,32)
#         output = _lenet5(output)
#         output = nn.Linear(10, 2)(F.relu(output))
#         return output

class LSTM_RNN(nn.Module):
    def __init__(self, input_size):
        super(LSTM_RNN, self).__init__()
        

    def forward(self, x):
        pass


class Net_clf:
    def __init__(self, net, input_len, lr=0.001, epoch):
        self.net = net(input_len)
        self.epoch = epoch
        self.criterion = nn.CrossEntropyLoss()
        self.optimizer = optim.SGD(self.net.parameters(), lr = lr)

    def train(self, train_loader):
        for epoch in range(self.epoch):
            for batch_idx, data in enumerate(train_loader):
                inputs, labels = data
                self.optimizer.zero_grad()
                outputs = self.net(inputs)
                loss = self.criterion(outputs, labels)
                loss.backward()
                self.optimizer.step()

    def test(self, test_loader):
        correct = 0
        total = 0
        with torch.no_grad():
            for data in test_loader:
                inputs, labels = data
                outputs = self.net(inputs)
                _, predict = torch.max(outputs.data, 1)
                total += labels.size(0)
                correct += (predict == labels).sum().item()
        print("Acc:{.3f}".format(100*correct / total))





