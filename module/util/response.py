#/usr/bin/env python
# -*- coding: utf-8 -*-
# 成員：簡立軒, 黃禎智, 楊筱筠
'''
Created on 2022年1月2日

@author: 簡立軒, 黃禎智, 楊筱筠
'''
from flask import Response
import json
from typing import Any

def set(status: int = -1, message: str = '', message_desc: str = '', data: Any = []) -> Response:
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