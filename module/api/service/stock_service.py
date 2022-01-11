#/usr/bin/env python
# -*- coding: utf-8 -*-
# 成員：簡立軒, 黃禎智, 楊筱筠
'''
Created on 2022年1月2日

@author: 簡立軒, 黃禎智, 楊筱筠
'''
from werkzeug.local import LocalProxy
from module.util import request
from module.util import constants as const
from module.util import audit
from module.prediction import model
from module.prediction import plot
from module.prediction import series as series_module

import asyncio
import logging, json, re, sys
import torch
import pandas as pd
import mplfinance as mpf
from torch.utils.data import DataLoader, TensorDataset
from datetime import datetime
from typing import Tuple, List, Dict, Any

LOG = logging.getLogger(__name__)
sys.setrecursionlimit(5000) # set recursion limit higher to avoid maximum recursion depth exceeded, default is 1000

stocks = {}

async def get_stocks(req: LocalProxy) -> Tuple[Dict, str]:

    # check parameter
    parameter = {}
    resStartDate = req.args.get('startdate')
    resEndDate = req.args.get('enddate')
    if not resStartDate:
        return {}, audit.input_error("startdate")
    if not resEndDate:
        return {}, audit.input_error("enddate")
    
    # set parameter
    parameter.update({"response": "json"})
    parameter.update({"type": "ALL"})
    resStartDate = int(resStartDate)
    resEndDate = int(resEndDate)
    if resEndDate < resStartDate:
        return {}, audit.request_error("end date must bigger than start date")
    
    # prepare for coroutine
    global stocks
    stocks = {}
    
    tasks = [stock_job(parameter, date) for date in range(resStartDate, resEndDate+1)]
    tasks1 = [raise_error(_) for _ in range(resStartDate, resEndDate+1)]
    
    _ = await asyncio.gather(*tasks, *tasks1, return_exceptions=True)
    
    return stocks, ''

async def raise_error(_) -> ValueError:
    raise ValueError
    
async def get_stock(req: LocalProxy, stockCode: str) ->Tuple[List, str]:

    stocks, err = await get_stocks(req)
    if err:
        return [], err
    
    pack = []
    for date, stock in stocks.items():
        if stock.get(stockCode):
            dt = datetime.strptime(str(date), "%Y%m%d")
            dt = datetime.strftime(dt, "%Y-%m-%d")
            stock[stockCode].update({"Date": dt})
            pack.append(stock[stockCode])
            
    df = None
    try:     
        df = to_data_frame_and_save(pack, stockCode=stockCode)
    except Exception as e:
        return {}, audit.exception(str(e))

    # 畫 k 線圖並儲存
    try:
        draw_and_save_k_graph(df=df, stockCode=stockCode)
    except Exception as e:
        return {}, audit.exception(str(e))
    
    # 上傳至imgur圖床
    result = None
    try:
        result = upload_to_imgur(pack, stockCode)
    except Exception as e:
        return {}, audit.exception(str(e))
    
    if not result:
        return {}, audit.exception('empty result')
            
    return result, ''

async def stock_job(parameter: dict, date: int) -> Tuple[str, str]:
    global stocks # load global stocks, sharing memory with all threads
    LOG.info(date)
    parameter.update({'date': date}) # makesure date is updated
    # do request
    res, err = request.call(
        "POST", const.TWSE_EXCHANGE_REPORT_URL,
        parameter=parameter,
    )
    
    # check response
    if err: 
        return '', err
    
    # set header title
    fields = {
        "成交股數": "Capacity",
        "成交筆數": "Transaction",
        "成交金額": "Turnover",
        "開盤價": "Open",
        "最高價": "High",
        "最低價": "Low",
        "收盤價": "Close",
        "漲跌價差": "Change"
    }
    # data9 storaging stock info, fields9 storaging header
    if not res.get('data9'):
        return
    for data in res['data9']:
        stock = {} # reset
        pattern = re.compile(r'[-]')
        found_negative = False
        for idx, field in enumerate(res['fields9']):
            # check if there exist negative data.
            if pattern.search(field):
                found_negative = pattern.search(data[idx])
                
            if field in fields:
                # set pattern
                pattern_a = '.' in data[idx] and ',' in data[idx]
                pattern_b = '.' in data[idx]
                pattern_c = ',' in data[idx]
                # convert data to correct type
                if pattern_a: data[idx] = float(data[idx].replace(',', ''))
                elif pattern_b: data[idx] = float(data[idx])
                elif pattern_c: data[idx] = int(data[idx].replace(',', ''))
                
                if fields[field] == 'Change' and found_negative:
                    stock.update({fields[field]: -data[idx]})
                else:
                    stock.update({fields[field]: data[idx]})
        
        # init date to stocks if not existing in stocks yet, otherwise append it
        # data[0] is stock code
        if stocks.get(date):
            stocks[date].update({data[0]: stock})
        else:
            stocks[date] = {}
            stocks[date].update({data[0]: stock})
            
    return 'Done', ''
            
def predict_stock_price(req: LocalProxy) -> Tuple[Dict, Any]:
    
    # load body
    body = {}
    try:
        body = json.loads(request.read(req.stream))
    except:
        pass
    
    # check parameters
    if not body.get('stockCode'):
        return {}, audit.input_error("stockCode")
    stockCode = body['stockCode']
    
    train = False
    if body.get('train'):
       train = True if body['train'] else False
    
    # load hyper parameters from env
    hyperParam = {
        "daysNum": int(const.DAYS_NUM),
        "epoch": int(const.EPOCH),
        "featuresSize": int(const.FEATURES),
        "hiddenSize": int(const.HIDDEN_SIZE),
        "outputSize": int(const.OUTPUT_SIZE),
        "batchSize": int(const.BATCH_SIZE),
        "earlyStop": int(const.EARLY_STOP),
        "learningRate": float(const.LEARNING_RATE)
    }
    LOG.info(hyperParam)

    # data processing
    series = series_module.Series(stockCode)
    data = series.get_series()
    feature, label = series.process_series(data, hyperParam['daysNum'])
    boundary = int(len(feature) * 0.8) # 80% for train, 20% for test
    xTrain = feature[:boundary]
    yTrain = label[:boundary]
    xTest = feature[boundary:]
    yTest = label[boundary:]

    # transfor data to tensor
    xTrain = torch.tensor(xTrain)
    xTest = torch.tensor(xTest)
    yTrain = torch.tensor(yTrain)
    yTest = torch.tensor(yTest)

    # init model
    net = model.Model(stockCode, hyperParam)
    
    # combine input and label by batch size using DataLoader
    testDataLoader = DataLoader(
        TensorDataset(xTest, yTest), hyperParam['batchSize'])
    
    if train:
        # combine input and label by batch size using DataLoader
        trainDataLoader = DataLoader(
            TensorDataset(xTrain, yTrain), hyperParam['batchSize'])
        # do train
        net.train_model(trainLoader=trainDataLoader, testLoader=testDataLoader)
        
    # do predict
    testData, testLabel = net.test_model(loader=testDataLoader)

    # draw for predicted and real data
    real = [element * (series.close_max - series.close_min) + series.close_min for element in testData]
    test = [element * (series.close_max - series.close_min) + series.close_min for element in testLabel]
    plot.draw(originalData=real, testData=test, savePath=f"/file/{stockCode}.png")
    
    # upload image to Imgur.
    imgur = plot.Imgur()
    image = imgur.upload(imgPath=f"/file/{stockCode}.png", name=stockCode)
    result = {
        "image": image,
        "predict": test[-1]
    }
    
    return result, ''

# draw k線圖 for stocks
def draw_and_save_k_graph(df: pd.DataFrame, stockCode: str) -> None:
    # set mpf attr
    marketcolors = mpf.make_marketcolors(up='r',down='g',inherit=True)
    style  = mpf.make_mpf_style(base_mpf_style='yahoo',marketcolors=marketcolors)
    # set kwargs，並在變數中填上繪圖時會用到的設定值
    kwargs = dict(type='candle', mav=(5,20,60), volume=True, figratio=(5,4), figscale=1, title=stockCode, style=style) 

    # 選擇df資料表為資料來源，帶入kwargs參數，畫出目標股票的走勢圖
    mpf.plot(df, **kwargs, savefig=f'module/api/file/{stockCode}_K.png')
    
# convert to data frame and save to local storage
def to_data_frame_and_save(pack: list, stockCode: str) -> pd.DataFrame:
    # set header
    name_attribute = [
    'Date', 'Capacity', 'Turnover', 'Open', 'High', 'Low', 'Close', 'Change',
    'Trascation'
    ]
    
    df = pd.DataFrame(columns=name_attribute, data=pack)
    df['Date'] = pd.to_datetime(df['Date'], format="%Y-%m-%d") # 轉換str to Datetime
    df.to_csv(f'module/data/{stockCode}.csv') # save data
    df.index = pd.DatetimeIndex(df['Date']) # 設置 index 為 Datetime
    df.rename(columns={'Turnover':'Volume'}, inplace = True)  # 針對資料表做修正，交易量(Turnover)在mplfinance中須被改為Volume才能被認出來
    return df

# 上傳
def upload_to_imgur(pack, stockCode) -> Dict:
    # upload image to Imgur.
    imgur = plot.Imgur()
    image = imgur.upload(imgPath = f"/../api/file/{stockCode}_K.png", name=stockCode)
    result = {
        "image": image,
        "data": pack
    }
    return result