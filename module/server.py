#/usr/bin/env python
# -*- coding: utf-8 -*-
# 成員：簡立軒, 黃禎智, 楊筱筠
'''
Created on 2022年1月2日

@author: 簡立軒, 黃禎智, 楊筱筠
'''

from module.util import log
from module.api.controller import route

from flask import Flask
from flask_restful_swagger_2 import Api
from flask_cors import CORS

conf={}
conf['verbose'] = 'DEBUG'
conf['log_path'] = 'logs/'
log.setup_logging(conf)

# base on WSGI
api = Flask(__name__)
CORS(api)  #全域性方式讓所有route都支援跨域，實現共享資源
#TODO: 更好的辦法應該是把json存成volume，透過docker-compose在run的時候直接讓swagger-ui掛載volume，即可透過底層docker直接實現
restful_set = Api(api,
    host='0.0.0.0:9234',
    schemes=['http'],
    api_version='v1.0',
    api_spec_url='/api/v1',
)
    
route.setup_route(restful_set)
