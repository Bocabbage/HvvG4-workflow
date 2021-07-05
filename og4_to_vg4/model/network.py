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


class Net_clf:
    def __init__(self, net, input_len, lr=0.001, epoch=10):
        self.net = net(input_len)
        self.epoch = epoch
        self.criterion = nn.CrossEntropyLoss()
        self.optimizer = optim.SGD(self.net.parameters(), lr=lr)

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