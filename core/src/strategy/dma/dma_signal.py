from strategy.trade_signal import TradeSignal, TradeSignalState
from constants import STRATEGY_DMA_SHORT_TERM, STRATEGY_DMA_LONG_TERM

class DMATradeSignal(TradeSignal):
    """Double MA strategy trade signal class"""

    def __init__(self, short_price=0, long_price=0, close_price=0, trade_date='', trade_days=0, trade_profit=0, message='', **kwargs):
        super().__init__(**kwargs)
        self.short = STRATEGY_DMA_SHORT_TERM
        self.long = STRATEGY_DMA_LONG_TERM
        self.short_price = short_price
        self.long_price = long_price
        self.close_price = close_price
        self.trade_date = trade_date
        self.trade_days = trade_days
        self.trade_profit = trade_profit
        self.message = message

    def get_message(self):
        if self.message != '':
            return self.message
        if self.state == TradeSignalState.BUY:
            self.message = super().get_message() + "收盘价" + str(self.close_price) + ", " + self.short + "日均线" + str(self.short_price) + ", " + self.long + "日均线" + str(self.long_price)
        elif self.state == TradeSignalState.SELL:
            self.message = super().get_message() + "收盘价" + str(self.close_price) + ", " + self.short + "日均线" + str(self.short_price) + ", " + self.long + "日均线" + str(self.long_price)
        elif self.state == TradeSignalState.HOLD:
            self.message = super().get_message() + "于" + self.trade_date + "日买入, " + "持有" + str(self.trade_days) + "天, 盈利" + str(round(self.trade_profit * 100, 2)) + "%"
        elif self.state == TradeSignalState.EMPTY:
            self.message = super().get_message() + "于" + self.trade_date + "日卖出, " + "空仓" + str(self.trade_days) + "天, 空仓期涨幅" + str(round(self.trade_profit * 100, 2)) + "%"
        return self.message