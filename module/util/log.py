#/usr/bin/env python
# -*- coding: utf-8 -*-
# 成員：簡立軒, 黃禎智, 楊筱筠
'''
Created on 2022年1月2日

@author: 簡立軒, 黃禎智, 楊筱筠
'''
import os
import errno
import logging.config

# setop logging config by dictConfig
def setup_logging(conf):
    log_dict = {
        'version': 1,
        'disable_existing_loggers': False,
        'root': {
            'level': 'DEBUG',
            'handlers': ['console', 'file']
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'detail',
                'level': conf['verbose']
            },
            'file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'formatter': 'detail',
                'level': conf['verbose'],
                'filename': '%s/info.log' % conf['log_path'],
                'maxBytes': 10 * 1024 * 1024,
                'backupCount': 10
            }
        },
        'formatters': {
            'detail': {
                'format': u'[%(asctime)s][%(process)d][%(threadName)10.10s]'
                '[%(levelname).1s][%(filename)s:%(funcName)s:%(lineno)s] :'
                ' %(message)s'
            },
            'simple': {
                'format': u'[%(asctime)s][%(process)d][%(threadName)10.10s]'
                '[%(levelname).1s][%(filename)s:%(lineno)s] : %(message)s'
            }
        }
    }
    # mkdir if log path isn't exist.
    ''' python 2
    if not os.path.exists(conf['log_path']):
        os.makedirs(conf['log_path'])
    '''
    try:
        os.makedirs(conf['log_path'])
    except OSError as problem:
        if problem.errno != errno.EEXIST:
            raise
        
    logging.config.dictConfig(log_dict)