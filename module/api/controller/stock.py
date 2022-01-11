#/usr/bin/env python
# -*- coding: utf-8 -*-
# 成員：簡立軒, 黃禎智, 楊筱筠
'''
Created on 2022年1月2日

@author: 簡立軒, 黃禎智, 楊筱筠
'''
from flask import request, Response
from flask_restful_swagger_2 import Resource

from module.api.service import stock_service
from module.util import response as resp

import asyncio

class GetStocks(Resource):
    """
    @parameter:   startdate
     required:    YES
     length:      8
     description: 搜尋日(起), %Y%m%d
    @parameter:   enddate
     required:    YES
     length:      8
     description: 搜尋日(訖), %Y%m%d
    @return
    """
    def get(self) -> Response:
        try:
            new_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(new_loop)
            loop = asyncio.get_event_loop()
            task = asyncio.ensure_future(stock_service.get_stocks(request))
            loop.run_until_complete(asyncio.wait([task]))
            res, err = task.result()
        except Exception as err:
            return resp.set(status=-1, message='error', message_desc=str(err))

        if err:
            return resp.set(status=-1, message='failed', message_desc=err)
        
        return resp.set(status=0, message='success', message_desc=err, data=res)
    
class GetStock(Resource):
    """
    @url_param:   stockCode
     required:    YES
     length:      -
     description: 股票代碼
    @parameter:   startdate
     required:    YES
     length:      8
     description: 搜尋日(起), %Y%m%d
    @parameter:   enddate
     required:    YES
     length:      8
     description: 搜尋日(訖), %Y%m%d
    @return
    """
    def get(self, stockCode: str) -> Response:
        try:
            new_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(new_loop)
            loop = asyncio.get_event_loop()
            task = asyncio.ensure_future(stock_service.get_stock(request, stockCode))
            loop.run_until_complete(asyncio.wait([task]))
            res, err = task.result()
        except Exception as err:
            return resp.set(status=-1, message='error', message_desc=str(err))

        if err:
            return resp.set(status=-1, message='failed', message_desc=err)
        
        return resp.set(status=0, message='success', message_desc=err, data=res)
    
class PredictStockPrice(Resource):
    """
    @url_param:   stockCode
     required:    YES
     length:      -
     description: 股票代碼
    @parameter:   train
     required:    NO
     length:      5 in MAX(bool: true/false)
     description: 是否訓練, flase則使用最近一次的模型
    """
    def post(self) -> Response:
        try:
            res, err = stock_service.predict_stock_price(request)
        except Exception as err:
            return resp.set(status=-1, message='error', message_desc=str(err))

        if err:
            return resp.set(status=-1, message='failed', message_desc=str(err))
        
        return resp.set(status=0, message='success', message_desc=str(err), data=res)