#/usr/bin/env python
# -*- coding: utf-8 -*-
# 成員：簡立軒, 黃禎智, 楊筱筠
'''
Created on 2022年1月2日

@author: 簡立軒, 黃禎智, 楊筱筠
'''

import torch
import torch.nn as nn
import torch.optim as optim
from tqdm import tqdm
from copy import deepcopy
from torch.utils.data import DataLoader
from typing import List, Tuple, Any
import os

_absPath = os.path.dirname(os.path.abspath(__file__))
    
class GRUNet(nn.Module):
    def __init__(self, inputSize, hiddenSize, outputFeafures) -> None:
        super().__init__()
        self.rnn = nn.GRU(
            input_size=inputSize,
            hidden_size=hiddenSize,
            num_layers=1,
            batch_first=True,
            bidirectional=True
        )
        self.out = nn.Sequential(
            nn.Linear(in_features=hiddenSize*2, out_features=outputFeafures, bias=True)
        )
        
    def forward(self, x):
        # 返回output, (h_n, c_n)(h_n, c_n) 表示 最後一層 hidden layer 的狀態
        r_out, (h_n, c_n) = self.rnn(x, None)
        # output 包含每一個時刻的輸出特徵，如果設定了 batch_first, 則batch為第一維, 取用最後一刻的輸出作為輸出層的輸入
        out = self.out(r_out[:, -1])
        return out

class Model:
    def __init__(self, stockCode: str, hyperParam: dict) -> None:
        # 超級參數
        self.daysNum = hyperParam['daysNum'] # 取幾天作為連續資料: 5
        self.epoch = hyperParam['epoch'] # 50 # 迭代次數
        self.featuresSize = hyperParam['featuresSize'] # 5 # input的特徵數量
        self.hiddenSize = hyperParam['hiddenSize'] # 128 # 隱藏層的層數
        self.outputSize = hyperParam['outputSize'] # 1 # 輸出層的size
        self.batchSize = hyperParam['batchSize'] # 20 # 批次size
        self.earlyStop = hyperParam['earlyStop'] # 5 # 指定情況下, 世代數記數大於此數, 終止訓練, 用來避免overfitting
        self.learningRate = hyperParam['learningRate'] # 0.001 # 學習率, 使其梯度偏移漸小, 大小與速度呈正比, 與精準度成反比
        self.stockCode = stockCode # 股票代碼, 用來區隔每次訓練的股別
        
        # 生成類神經網絡, 使用單層單向的 LSTM 網路，輸出使用全連接層的 Linear 網路
        self.model = GRUNet(
            inputSize=self.featuresSize,
            hiddenSize=self.hiddenSize,
            outputFeafures=self.outputSize
        )
        
        # lost function 使用 MSE func.(均方誤差 mean-square error), 用來評估資料變化程度
        self.loss_func = nn.MSELoss()
        # optimization algorithm, 使用 Adam. 每次更新都會調整新舊gradient的權重, 本質是RMSProp+Momentum, 每次的sigma都和前一次的有關係
        self.optimizer = optim.Adam(self.model.parameters(), lr=self.learningRate, weight_decay=0.001)

    def train_model(self, 
            trainLoader: DataLoader[Tuple[torch.Tensor, ...]], 
            testLoader: DataLoader[Tuple[torch.Tensor, ...]]
        ) -> None:
        # initial parameters
        bestModel = None
        trainLoss = 0
        testLoss = 0
        bestLoss = 100
        epochCount = 0
        
        for epoch in range(self.epoch):
            # initial loss rate
            totalTrainLoss = 0
            totalTrainNum = 0
            totalTestLoss = 0
            totalTestNum = 0
            
            for x, y in tqdm(trainLoader, desc=f'Epoch: {epoch}| Train Loss: {trainLoss}| Test Loss: {testLoss}'):
                numX = len(x)
                y = y.float()
                
                # forward
                p = self.model(x)
                loss = self.loss_func(p, y) # 計算誤差值
                # backward
                self.optimizer.zero_grad() # 將梯度歸零
                loss.backward() # 反向傳播
                self.optimizer.step() # 更新參數
                # loss calculate
                totalTrainLoss += loss.item()
                totalTrainNum += numX
            trainLoss = totalTrainLoss / totalTrainNum
            
            for x, y in testLoader:
                numX = len(x)
                y = y.float()
                # forward
                p = self.model(x)
                loss = self.loss_func(p, y) # 計算誤差值
                # backward
                self.optimizer.zero_grad() # 將梯度歸零
                loss.backward() # 反向傳播
                self.optimizer.step() # 更新參數
                # loss calculate
                totalTestLoss += loss.item()
                totalTestNum += numX
            testLoss = totalTestLoss / totalTestNum
            
            # 當當前最小誤差值(bestLoss)連續數次(self.earlyStop)比最新測試結果誤差值大, 則終止提早訓練
            # 當當前最小誤差值仍比最新測試結果誤差值大時，將當前model設為bestModel且取代原最小誤差值
            if bestLoss > testLoss:
                bestLoss = testLoss
                bestModel = deepcopy(self.model) # 使用 deepcopy 避免資料髒掉
                epochCount = 0 # 重置epoch計算，僅有連續次數超過self.earlyStop次數時才會進行count計算
            else:
                epochCount += 1
                
            if epochCount > self.earlyStop:
                torch.save(bestModel.state_dict(), f'{_absPath}/trained_model/{self.stockCode}.pth')
                break
            
    def test_model(self, loader: DataLoader[Tuple[torch.Tensor, ...]]) -> Tuple[List, List, float]:
        result = []
        label = []
        
        model = GRUNet(
            inputSize=self.featuresSize,
            hiddenSize=self.hiddenSize,
            outputFeafures=self.outputSize
        )
        model.load_state_dict(torch.load(f"{_absPath}/trained_model/{self.stockCode}.pth")) # 讀取模型
        model.eval() # 切換為評估模式
        
        totalTestLoss = 0
        totalTestNum = 0
        for x, y in loader:
            numX = len(x)
            y = y.float() # label
            predictedData = model(x)
            loss = self.loss_func(predictedData, y)
            totalTestLoss += loss.item()
            totalTestNum += numX
            result.extend(predictedData.data.squeeze(1).tolist())
            label.extend(y.tolist())
        testLoss = totalTestLoss / totalTestNum
        
        return result, label

    def predict_model(self, x:torch.Tensor) -> List:
        model = GRUNet(
            inputSize=self.featuresSize,
            hiddenSize=self.hiddenSize,
            outputFeafures=self.outputSize
        )
        model.load_state_dict(torch.load(f"{_absPath}/trained_model/{self.stockCode}.pth"))
        model.eval() # 切換為評估模式
        
        predictedData = model(x)
        result = predictedData.data.squeeze(1).tolist() # 透過squeeze去掉第二維度中所有為1的維度, 目的是數據的可視化及還原

        return result