import talib as ta
import numpy as np
import tushare as ts
from datetime import datetime, timedelta
import os
from constants import TODAY_STR

pro = ts.pro_api(os.environ['TUSHARE_API_TOKEN'])

SHORT_TERM = 11
LONG_TERM = 22
MAX_DAYS = 150

start = (datetime.today() - timedelta(days=MAX_DAYS)).strftime('%Y%m%d')
end = TODAY_STR

def double_ma_strategy(code, name):
    print('start calculating target for %s(%s)' % (name, code))
    adj = pro.fund_adj(ts_code=code, start_date=start, end_date=end).sort_index(ascending=False)
    data = pro.fund_daily(ts_code=code, start_date=start, end_date=end).sort_index(ascending=False)
    data = data.merge(adj, on='trade_date')
    try:
        qfq_close_price = data['close'].multiply(data['adj_factor']) / data['adj_factor'].iloc[-1]
    except:
        return 'X', code, name, 'cannot get price by ts'
    close_price = np.array(qfq_close_price)
    time = np.array(data['trade_date'])
    short_ma = np.round(ta.MA(close_price, SHORT_TERM), 3)
    long_ma = np.round(ta.MA(close_price, LONG_TERM), 3)
    if (short_ma[-1] > long_ma[-1] and short_ma[-2] <= long_ma[-2]):
        message = name + "(" + str(code) + ")" + "可买, 收盘价" + str(close_price[-1]) + ", 11日均线" + str(short_ma[-1]) + ", 22日均线" + str(long_ma[-1])
        return 'B', code, name, message
    elif (short_ma[-1] < long_ma[-1] and short_ma[-2] >= long_ma[-2]):
        message = name + "(" + str(code) + ")" + "可卖, 收盘价" + str(close_price[-1]) + ", 11日均线" + str(short_ma[-1]) + ", 22日均线" + str(long_ma[-1])
        return 'S', code, name, message
    else:
        if short_ma[-1] > long_ma[-1]:
            find_buy_day = len(long_ma) - 1
            for i in range(1, len(long_ma)):
                if short_ma[-1 - i] <= long_ma[-1 - i]:
                    find_buy_day = i
                    break
            s = datetime.strptime(time[-1 - find_buy_day], '%Y%m%d')
            e = datetime.strptime(time[-1], '%Y%m%d')
            interval_days = (e - s).days
            message = name + "(" + str(code) + ")" + "于" + str(time[-1 - find_buy_day]) + "日买入, " + "持有" + str(interval_days) + "天, 盈利" + str(round((close_price[-1] - close_price[-1 - find_buy_day]) / close_price[-1 - find_buy_day] * 100, 2)) + "%"
            return 'H', code, name, message
        if short_ma[-1] < long_ma[-1]:
            find_sell_day = len(long_ma) - 1
            for i in range(1, len(long_ma)):
                if short_ma[-1 - i] >= long_ma[-1 - i]:
                    find_sell_day = i
                    break
            s = datetime.strptime(time[-1 - find_sell_day], '%Y%m%d')
            e = datetime.strptime(time[-1], '%Y%m%d')
            interval_days = (e - s).days
            message = name + "(" + str(code) + ")" + "于" + str(time[-1 - find_sell_day]) + "日卖出, " + "空仓" + str(interval_days) + "天, 空仓期涨幅" + str(round((close_price[-1] - close_price[-1 - find_sell_day]) / close_price[-1 - find_sell_day] * 100, 2)) + "%"
            return 'E', code, name, message
    return 'X', code, name, 'state error, 11日均线价格 %s(前一天价格为%s), 22日均线价格 %s(前一天价格为%s)' % (str(short_ma[-1]), str(short_ma[-2]), str(long_ma[-1]), str(long_ma[-2]))