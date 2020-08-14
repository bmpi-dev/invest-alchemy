try:
  import unzip_requirements
except ImportError:
  pass
import json
import talib as ta
import numpy as np
import tushare as ts
import matplotlib.pyplot as plt
import pandas as pd
import os
from datetime import datetime, timedelta

def init():
    pro = ts.pro_api(os.environ['TUSHARE_API_TOKEN'])

    start = (datetime.today() - timedelta(days=150)).strftime('%Y%m%d')
    end = datetime.today().strftime('%Y%m%d')

    short_term = 11
    long_term = 22

    buy_codes = []
    sell_codes = []
    hold_codes = []
    empty_codes = []

def run(code, name):
    data = pro.fund_daily(ts_code=code, start_date=start, end_date=end).sort_index(ascending=False)
    close_price = np.array(data['close'])
    time = np.array(data['trade_date'])
    short_ma = np.round(ta.MA(close_price, short_term), 3)
    long_ma = np.round(ta.MA(close_price, long_term), 3)
    if (short_ma[-1] > long_ma[-1] and short_ma[-2] <= long_ma[-2]):
        s = name + "(" + str(code) + ")" + "可买, 收盘价" + str(close_price[-1]) + ", 11日均线" + str(short_ma[-1]) + ", 22日均线" + str(long_ma[-1])
        buy_codes.append(s)
    elif (short_ma[-1] < long_ma[-1] and short_ma[-2] >= long_ma[-2]):
        s = name + "(" + str(code) + ")" + "可卖, 收盘价" + str(close_price[-1]) + ", 11日均线" + str(short_ma[-1]) + ", 22日均线" + str(long_ma[-1])
        sell_codes.append(s)
    else:
        if short_ma[-1] > long_ma[-1]:
            for i in range(1, len(long_ma)):
                if short_ma[-1 - i] <= long_ma[-1 - i]:
                    s = datetime.strptime(time[-1 - i], '%Y%m%d')
                    e = datetime.strptime(time[-1], '%Y%m%d')
                    interval_days = (e - s).days
                    s = name + "(" + str(code) + ")" + "于" + str(time[-1 - i]) + "日买入, " + "持有" + str(interval_days) + "天, 盈利" + str(round((close_price[-1] - close_price[-1 -i]) / close_price[-1 -i] * 100, 2)) + "%"
                    hold_codes.append(s)
                    break
        if short_ma[-1] < long_ma[-1]:
            for i in range(1, len(long_ma)):
                if short_ma[-1 - i] >= long_ma[-1 - i]:
                    s = datetime.strptime(time[-1 - i], '%Y%m%d')
                    e = datetime.strptime(time[-1], '%Y%m%d')
                    interval_days = (e - s).days
                    s = name + "(" + str(code) + ")" + "于" + str(time[-1 - i]) + "日卖出, " + "空仓" + str(interval_days) + "天, 空仓期涨幅" + str(round((close_price[-1] - close_price[-1 -i]) / close_price[-1 -i] * 100, 2)) + "%"
                    empty_codes.append(s)
                    break

def invest(event, context):
    with open("fund.txt", "r") as f:
        for line in f:
            code_name = line.split(",")
            run(code_name[0], code_name[1].rstrip())
    
    print('可买标的:')
    for code in buy_codes:
        print(code)
    print('#########################################')
    print('可卖标的:')
    for code in sell_codes:
        print(code)
    print('#########################################')
    print('持仓标的:')
    for code in hold_codes:
        print(code)
    print('#########################################')
    print('空仓标的:')
    for code in empty_codes:
        print(code)
    
    response = {
        "statusCode": 200,
    }

    return response
