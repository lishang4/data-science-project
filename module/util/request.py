#/usr/bin/env python
# -*- coding: utf-8 -*-
# 成員：簡立軒, 黃禎智, 楊筱筠
'''
Created on 2022年1月2日

@author: 簡立軒, 黃禎智, 楊筱筠
'''
from . import audit
from . import constants as cts
import requests
import json
import logging
LOG = logging.getLogger(__name__)

def call(method: str = "POST", url: str="", header: dict={}, payload: dict={}, parameter: dict={}):
    """
    Note: 
    @parameter: method
    @parameter: url
    @parameter: header
    @parameter: payload
    @parameter: parameter
    @return
    """
    
    payload = json.dumps(payload, ensure_ascii=False)
    payload = payload.encode('utf-8')
    r_obj = None
    try:
        r_obj = requests.request(
            method, 
            url, 
            headers=header,
            params=parameter,
            timeout=float(cts.REQUEST_TIMEOUT)
        )
    except requests.Timeout:
        LOG.error(f"Timeout connection to server.")
        return '', audit.request_error('TIMEOUT')
    except Exception as e:
        LOG.error(f"Error accessing server: {str(e)}")
        return '', audit.request_error('ERROR_ACCESSING')

    if r_obj:
        if r_obj.status_code in [401, 403]:
            msg = f"Received {r_obj.status_code}, API Authentication Failed."
            return r_obj, audit.request_error(msg)

        elif r_obj.status_code not in [200]:
            msg = f"Received {r_obj.status_code} error from server."
            return r_obj, audit.request_error(msg)

    # load
    try:
        res = r_obj.json()
    except ValueError:
        return '', audit.request_error(ValueError)
    except Exception as e:
        return '', audit.request_error(e)

    return res, ''

# read request as utf-8
def read(request_stream: str) -> str:
    try:
        return request_stream.read().decode('utf-8')
    except Exception as e:
        return e