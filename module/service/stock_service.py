#/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2021年11月22日

@author: lishangchien, A Y
'''
from module.util import request
from module.util import constants as const
from module.util import audit
import threading
import logging
LOG = logging.getLogger(__name__)

stocks = {}

def get_stocks(req):

    # check parameter
    parameter = {}
    resStartDate = req.args.get('startdate')
    resEndDate = req.args.get('enddate')
    if not resStartDate:
        return '', audit.input_error("startdate")
    if not resEndDate:
        return '', audit.input_error("enddate")
    
    # set parameter
    parameter.update({"response": "json"})
    parameter.update({"type": "ALL"})
    resStartDate = int(resStartDate)
    resEndDate = int(resEndDate)
    
    # prepare threads
    global stocks
    
    # init global data
    stocks = {}
    threads_set = []
    for date in range(resStartDate, resEndDate+1):
        # TODO: append redis here
        # set thread
        thread = threading.Thread(target=stock_job,args=(parameter,date,))
        threads_set.append(thread)
    
    # do thread
    for t in threads_set:
        t.start()
    # wait thread
    t.join()
    
    return stocks, ''
    
def get_stock(req, stockCode):

    stocks, err = get_stocks(req)
    if err:
        return '', err
    
    pack = []
    for date, stock in stocks.items():
        if stock.get(stockCode):
            stock[stockCode].update({"日期": date})
            pack.append(stock[stockCode])
            
    return pack, ''
    
lock = threading.Lock()

def stock_job(parameter: dict, date):
    global stocks
    lock.acquire()
    LOG.info(date)
    parameter.update({'date': date})
    res, err = request.call(
        "POST", const.TWSE_EXCHANGE_REPORT_URL,
        parameter=parameter,
    )
    lock.release()
    # check response
    if err: 
        return '', err
    
    # data9 storaging stock info, fields9 storaging header
    if not res.get('data9'):
        return
    for data in res['data9']:
        stock = {} # reset
        for idx, field in enumerate(res['fields9']):
            stock.update({field: data[idx]})
        
        # init date to stocks if not existing in stocks yet, otherwise append it
        if stocks.get(date):
            stocks[date].update({data[0]: stock})
        else:
            stocks[date] = {}
            stocks[date].update({data[0]: stock})