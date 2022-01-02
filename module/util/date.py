#/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2022年1月2日

@author: lishangchien
'''
from datetime import datetime

def to_date(dateStr: str) -> datetime:
    return datetime.strptime(dateStr, "%Y%m%d")

def get_week_day(date: datetime) -> int:
    #weekday()可以獲得是星期幾
    return date.weekday()