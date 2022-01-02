#/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2022年1月2日

@author: lishangchien
'''
import os

# name of environment variables
TWSE_EXCHANGE_REPORT_URL = os.environ.get("EASY_CARD_ADAPTER_IP", "https://www.twse.com.tw/exchangeReport/MI_INDEX")
REQUEST_TIMEOUT = os.environ.get("REQUEST_TIMEOUT", 10)