#/usr/bin/env python
# -*- coding: utf-8 -*-
# 成員：簡立軒, 黃禎智, 楊筱筠
'''
Created on 2022年1月2日

@author: 簡立軒, 黃禎智, 楊筱筠
'''
import os

# name of environment variables
TWSE_EXCHANGE_REPORT_URL = os.environ.get("EASY_CARD_ADAPTER_IP", "https://www.twse.com.tw/exchangeReport/MI_INDEX")
REQUEST_TIMEOUT = os.environ.get("REQUEST_TIMEOUT", "10")

# hyper parameters
DAYS_NUM = os.environ.get("DAYS_NUM", "5")
EPOCH = os.environ.get("EPOCH", "50")
FEATURES = os.environ.get("FEATURES", "5")
HIDDEN_SIZE = os.environ.get("HIDDEN_SIZE", "128")
OUTPUT_SIZE = os.environ.get("OUTPUT_SIZE", "1")
BATCH_SIZE = os.environ.get("BATCH_SIZE", "20")
EARLY_STOP = os.environ.get("EARLY_STOP", "5")
LEARNING_RATE = os.environ.get("LEARNING_RATE", "0.001")

# imgur parameters
CLIENT_ID = os.environ.get("CLIENT_ID", "46a3cbeb163bb81")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET", "04e825410c751051e6b548a7d2a1b86b42b449b0")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN", "74d37721f55f72efa151a19c6122d2cf9a9ab471")
REFRESH_TOKEN = os.environ.get("REFRESH_TOKEN", "6e4b2f4b8f563a68070432b8abd57cd69edc779a")
ALBUM = os.environ.get("ALBUM", "gezjl8K")