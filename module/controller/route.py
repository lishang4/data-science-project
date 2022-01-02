#/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2022年1月2日

@author: lishangchien
'''

from flask import (
    Response, request
)
from flask_restful_swagger_2 import (
    Resource
)
from . import stock

def setup_route(app):
    '''
    api routing
    '''
    
    app.add_resource(HealthyCheck, '/healthyCheck')

    app.add_resource(stock.GetStocks, '/api/v1/stocks')
    app.add_resource(stock.GetStock, '/api/v1/stock/<stockCode>')

class HealthyCheck(Resource):
    def get(self):
        return Response(
            {
                'status': '0', 
                'message': 'success'
            }, 
            status=200
        )