#/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2022年1月2日

@author: lishangchien
'''
from module.server import api

if __name__ == "__main__":
    api.run(host='0.0.0.0', port= 9234, debug=True)