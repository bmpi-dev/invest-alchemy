import talib as ta
import numpy as np
import tushare as ts
from datetime import datetime, timedelta
import os
from constants import TODAY_STR

pro = ts.pro_api(os.environ['TUSHARE_API_TOKEN'])

start = (datetime.today() - timedelta(days=150)).strftime('%Y%m%d')
end = TODAY_STR

short_term = 11
long_term = 22

def double_ma_strategy(code, name):
    print('start calculating code for %s' % code)
    adj = pro.fund_adj(ts_code=code, start_date=start, end_date=end).sort_index(ascending=False)
    data = pro.fund_daily(ts_code=code, start_date=start, end_date=end).sort_index(ascending=False)
    data = data.merge(adj, on='trade_date')
    try:
        qfq_close_price = data['close'].multiply(data['adj_factor']) / data['adj_factor'].iloc[-1]
    except:
        print("ERROR: cannot get price by ts, the code is " + code + " and will be skiped...\n")
        return 'X', code, name, ''
    close_price = np.array(qfq_close_price)
    time = np.array(data['trade_date'])
    short_ma = np.round(ta.MA(close_price, short_term), 3)
    long_ma = np.round(ta.MA(close_price, long_term), 3)
    if (short_ma[-1] > long_ma[-1] and short_ma[-2] <= long_ma[-2]):
        message = name + "(" + str(code) + ")" + "可买, 收盘价" + str(close_price[-1]) + ", 11日均线" + str(short_ma[-1]) + ", 22日均线" + str(long_ma[-1])
        return 'B', code, name, message
    elif (short_ma[-1] < long_ma[-1] and short_ma[-2] >= long_ma[-2]):
        message = name + "(" + str(code) + ")" + "可卖, 收盘价" + str(close_price[-1]) + ", 11日均线" + str(short_ma[-1]) + ", 22日均线" + str(long_ma[-1])
        return 'S', code, name, message
    else:
        if short_ma[-1] > long_ma[-1]:
            for i in range(1, len(long_ma)):
                if short_ma[-1 - i] <= long_ma[-1 - i]:
                    s = datetime.strptime(time[-1 - i], '%Y%m%d')
                    e = datetime.strptime(time[-1], '%Y%m%d')
                    interval_days = (e - s).days
                    message = name + "(" + str(code) + ")" + "于" + str(time[-1 - i]) + "日买入, " + "持有" + str(interval_days) + "天, 盈利" + str(round((close_price[-1] - close_price[-1 -i]) / close_price[-1 -i] * 100, 2)) + "%"
                    return 'H', code, name, message
        if short_ma[-1] < long_ma[-1]:
            for i in range(1, len(long_ma)):
                if short_ma[-1 - i] >= long_ma[-1 - i]:
                    s = datetime.strptime(time[-1 - i], '%Y%m%d')
                    e = datetime.strptime(time[-1], '%Y%m%d')
                    interval_days = (e - s).days
                    message = name + "(" + str(code) + ")" + "于" + str(time[-1 - i]) + "日卖出, " + "空仓" + str(interval_days) + "天, 空仓期涨幅" + str(round((close_price[-1] - close_price[-1 -i]) / close_price[-1 -i] * 100, 2)) + "%"
                    return 'E', code, name, message