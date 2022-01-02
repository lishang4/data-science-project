#/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2022年1月2日

@author: lishangchien
'''
from flask import Flask
from flask_restful_swagger_2 import Api
from flask_cors import CORS
from module.util import log
from module.controller import route

conf={}
conf['verbose'] = 'DEBUG'
conf['log_path'] = 'logs/'
log.setup_logging(conf)
api = Flask(__name__)
CORS(api)  #全域性方式讓所有route都支援跨域，實現共享資源
#TODO: 更好的辦法應該是把json存成volume，透過docker-compose在run的時候直接讓swagger-ui掛載volume，即可透過底層docker直接實現
restful_set = Api(api,
    host='0.0.0.0:9234',
    schemes=['http'],
   # base_path='/dev',
    api_version='v1.0',
    api_spec_url='/api/swagger',
    title='YouYou API',
    description='IO & route  documents',
    contact={
        "name": "Emotibot",
        "url": "http://www.emotibot.com",
        "email": "lishangchien@emotibot.com"
    },
    license={
        "name": "none",
        "url": "https://www.emotibot.com"
    })
    
route.setup_route(restful_set)
