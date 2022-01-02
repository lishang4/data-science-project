#/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2022年1月2日

@author: lishangchien
'''

# TODO: connect audit to logging

def input_error(parameter: str) -> str:
    return f'[InputError] missing "{parameter}" parameter.'

def request_error(error: str) -> str:
    return f'[RequestError] {except_raise(error)}'

# exception handler
def except_raise(e):
    error_class = e.__class__.__name__ #取得錯誤類型
    detail = e.args[0] #取得詳細內容
    cl, exc, tb = sys.exc_info() #取得Call Stack
    lastCallStack = traceback.extract_tb(tb)[-1] #取得Call Stack的最後一筆資料
    fileName = lastCallStack[0] #取得發生的檔案名稱
    lineNum = lastCallStack[1] #取得發生的行號
    funcName = lastCallStack[2] #取得發生的函數名稱
    errMsg = f"File \"{fileName}\", line {lineNum}, in {funcName}: [{error_class}] {detail}"
    return errMsg