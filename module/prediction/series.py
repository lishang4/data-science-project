#/usr/bin/env python
# -*- coding: utf-8 -*-
# 成員：簡立軒, 黃禎智, 楊筱筠
'''
Created on 2022年1月2日

@author: 簡立軒, 黃禎智, 楊筱筠
'''

import pandas as pd
from typing import Tuple, List
import os

_absPath = os.path.dirname(os.path.abspath(__file__))

class Series:
    def __init__(self, stockId) -> None:
        self.stockId = stockId
        self.series = None
        self.close_min = None
        self.close_max = None
    
    @staticmethod
    def standardization(data: pd.DataFrame) -> pd.Series:
         # standardization by formula: (x - min_x) / (max_x - min_x), also called MAX-MIN
        return data.apply(lambda x: (x- min(x)) / (max(x) - min(x)))
    
    def get_series(self, predict: bool = False) -> pd.Series:
        data = pd.read_csv(f'{_absPath}/../data/{self.stockId}_history.csv', parse_dates=True, index_col=1)
        data = data[["Open", "Close", "High", "Low", "Turnover"]]
        
        if not predict:
            self.close_min = data['Close'].min()
            self.close_max = data['Close'].max()
            
        self.series = self.standardization(data) # apply DataFrame to Series
        self.series.to_csv(f'{_absPath}/../data/{self.stockId}_series.csv')
        
        return self.series
    
    def process_series(self, series: pd.Series, n: int, predict: bool = False) -> Tuple[List, List]:
        
        # every n data will be combine to one series, will being the feature
        features = [
            series.iloc[i: i+n].values.tolist() 
            for i in range(len(series) -n + 2)
            if i +n < len(series)
        ]
        
        # every n data will be combine to one series, will being the feature
        label = []
        if not predict:
            label = [
                self.series.Close.values[i + n]
                for i in range(len(series) -n + 2)
                if i +n < len(series)
            ]
        
        return features, label