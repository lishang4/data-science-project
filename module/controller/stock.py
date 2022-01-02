#/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2022年1月2日

@author: lishangchien
'''
import logging
from flask import request
from flask_restful_swagger_2 import Resource

from module.service import stock_service
from module.util import response as resp

LOG = logging.getLogger(__name__)

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
    def get(self):
        try:
            res, err = stock_service.get_stocks(request)
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
    def get(self, stockCode):
        try:
            res, err = stock_service.get_stock(request, stockCode)
        except Exception as err:
            return resp.set(status=-1, message='error', message_desc=err)

        if err:
            return resp.set(status=-1, message='failed', message_desc=err)
        
        return resp.set(status=0, message='success', message_desc=err, data=res)