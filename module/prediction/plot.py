#/usr/bin/env python
# -*- coding: utf-8 -*-
# 成員：簡立軒, 黃禎智, 楊筱筠
'''
Created on 2022年1月2日

@author: 簡立軒, 黃禎智, 楊筱筠
'''

from module.util import constants as const
import matplotlib
import matplotlib.pyplot as plt
from imgurpython import ImgurClient
import os
from datetime import datetime
import logging

matplotlib.use('Agg') # set matplotlib to use Anti-Grain Geometry(C++ lib)
logging.getLogger('matplotlib').setLevel(logging.ERROR) # display matplotlib's log only if error show up

LOG = logging.getLogger(__name__)
_absPath = os.path.dirname(os.path.abspath(__file__))

# design pattern
class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

# using singleton to avoid client being created multiple times
class Imgur(metaclass=Singleton):
    """create imgur client automatic when class got init
    """
    def __init__(self) -> None:
        self.client_id = const.CLIENT_ID
        self.client_secret = const.CLIENT_SECRET
        self.access_token = const.ACCESS_TOKEN
        self.refresh_token = const.REFRESH_TOKEN
        self.album = const.ALBUM
        self.client = self.create_client()
    
    def create_client(self):
        return ImgurClient(self.client_id, self.client_secret, self.access_token, self.refresh_token)
    
    def upload(self, imgPath: str, name: str = 'stockCode') -> str:
        config = {
            'album':  self.album,
            'name': f"{name}_{datetime.now()}",
            'title': f"{name}_{datetime.now()}",
            'description': f'stock'
        }

        LOG.info("Uploading image... ")
        url = self.client.upload_from_path(f"{_absPath}{imgPath}", config=config, anon=False)
        LOG.info("Done")

        return url
    
def draw(originalData: list, testData: list, savePath: str) -> None:
    """save and clear fig after draw 

    Args:
        originalData (list): [blue line]
        testData (list): [green line]
        savePath (str): [fig save path]
    """
    # draw real data, tag to blue
    plt.plot(range(len(originalData)), originalData, color='b', label="real stock price")
    # draw predicted real data, tag to green, start from 1 because prediction is future's data
    plt.plot(range(1, len(testData)), testData[:-1], color='green', label="predicted real stock price")

    # draw future data, tag to red
    x_values = [len(testData)-1, len(testData)]
    y_values = [testData[-2], testData[-1]]
    plt.plot(x_values, y_values, color='r', label="predicted future stock price")
    
    plt.xlabel('Date', fontsize=18)
    plt.ylabel('Close', fontsize=18)
    plt.legend()
    #plt.show()
    plt.savefig(f"{_absPath}{savePath}")
    plt.clf()