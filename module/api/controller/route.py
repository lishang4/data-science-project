#/usr/bin/env python
# -*- coding: utf-8 -*-
# 成員：簡立軒, 黃禎智, 楊筱筠
'''
Created on 2022年1月2日

@author: 簡立軒, 黃禎智, 楊筱筠
'''

from flask import (
    Response
)
from flask_restful_swagger_2 import (
    Resource
)
from module.api.controller import stock

def setup_route(app) -> None:
    '''
    setup router
    '''
    
    app.add_resource(HealthyCheck, '/healthyCheck')

    app.add_resource(stock.GetStocks, '/api/v1/stocks')
    app.add_resource(stock.GetStock, '/api/v1/stock/<stockCode>')
    app.add_resource(stock.PredictStockPrice, '/api/v1/stock/predict/price')

class HealthyCheck(Resource):
    def get(self) -> Response:
        return Response(
            {
                'status': '0', 
                'message': 'success'
            }, 
            status=200
        )