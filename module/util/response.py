#/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2022年1月2日

@author: lishangchien
'''
from flask import (
    Response, request
)
import json

def set(status: int = -1, message: str = '', message_desc: str = '', data: any =[]):
    return Response(
        json.dumps(
            {
            'status': status,
            'message': message,
            'message_desc': message_desc,
            'data': data
            }
        )
    )