import talib as ta
import numpy as np
import tushare as ts
from datetime import datetime, timedelta
import os
from constants import TODAY_STR, STRATEGY_DMA_SHORT_TERM, STRATEGY_DMA_LONG_TERM
from strategy.dma.dma_signal import DMATradeSignal
from strategy.trade_signal import TradeSignalState
from strategy.trade_strategy import IStrategy

pro = ts.pro_api(os.environ['TUSHARE_API_TOKEN'])

MAX_DAYS = 150

start = (datetime.today() - timedelta(days=MAX_DAYS)).strftime('%Y%m%d')
end = TODAY_STR

class DMATradeStrategy(IStrategy):

    def __init__(self):
        self.__trade_signals = []

    @property
    def trade_signals(self):
        return self.__trade_signals

    def process(self, file_path):
        with open(file_path, "r") as f:
            for line in f:
                code_name = line.split(",")
                dma_trade_signal = self.__trade(code_name[0], code_name[1].rstrip())
                if dma_trade_signal.state == TradeSignalState.ERROR:
                    print('Error happened for %s(%s), message is %s' % (dma_trade_signal.name, dma_trade_signal.code, dma_trade_signal.message))
                self.__trade_signals.append(dma_trade_signal)

    def __trade(self, code, name):
        print('start calculating target for %s(%s)' % (name, code))
        adj = pro.fund_adj(ts_code=code, start_date=start, end_date=end).sort_index(ascending=False)
        data = pro.fund_daily(ts_code=code, start_date=start, end_date=end).sort_index(ascending=False)
        data = data.merge(adj, on='trade_date')
        try:
            qfq_close_price = data['close'].multiply(data['adj_factor']) / data['adj_factor'].iloc[-1]
        except:
            return DMATradeSignal(state=TradeSignalState.ERROR, code=code, name=name, message='cannot get price by ts')
        close_price = np.array(qfq_close_price)
        time = np.array(data['trade_date'])
        short_ma = np.round(ta.MA(close_price, STRATEGY_DMA_SHORT_TERM), 3)
        long_ma = np.round(ta.MA(close_price, STRATEGY_DMA_LONG_TERM), 3)
        if (short_ma[-1] > long_ma[-1] and short_ma[-2] <= long_ma[-2]):
            return DMATradeSignal(state=TradeSignalState.BUY, code=code, name=name, close_price=close_price[-1], short_price=short_ma[-1], long_price=long_ma[-1])
        elif (short_ma[-1] < long_ma[-1] and short_ma[-2] >= long_ma[-2]):
            return DMATradeSignal(state=TradeSignalState.SELL, code=code, name=name, close_price=close_price[-1], short_price=short_ma[-1], long_price=long_ma[-1])
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
                return DMATradeSignal(state=TradeSignalState.HOLD, code=code, name=name, trade_date=str(time[-1 - find_buy_day]), trade_days=interval_days, trade_profit=((close_price[-1] - close_price[-1 - find_buy_day]) / close_price[-1 - find_buy_day]))
            if short_ma[-1] < long_ma[-1]:
                find_sell_day = len(long_ma) - 1
                for i in range(1, len(long_ma)):
                    if short_ma[-1 - i] >= long_ma[-1 - i]:
                        find_sell_day = i
                        break
                s = datetime.strptime(time[-1 - find_sell_day], '%Y%m%d')
                e = datetime.strptime(time[-1], '%Y%m%d')
                interval_days = (e - s).days
                return DMATradeSignal(state=TradeSignalState.EMPTY, code=code, name=name, trade_date=str(time[-1 - find_sell_day]), trade_days=interval_days, trade_profit=((close_price[-1] - close_price[-1 - find_sell_day]) / close_price[-1 - find_sell_day]))
        error_message = 'state error, 11日均线价格 %s(前一天价格为%s), 22日均线价格 %s(前一天价格为%s)' % (str(short_ma[-1]), str(short_ma[-2]), str(long_ma[-1]), str(long_ma[-2]))
        return DMATradeSignal(state=TradeSignalState.ERROR, code=code, name=name, message=error_message)