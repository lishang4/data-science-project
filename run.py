#/usr/bin/env python
# -*- coding: utf-8 -*-
# 成員：簡立軒, 黃禎智, 楊筱筠
'''
Created on 2022年1月2日

@author: 簡立軒, 黃禎智, 楊筱筠
'''
from module.server import api

if __name__ == "__main__":
    api.run(host='0.0.0.0', port= 9234, debug=True)