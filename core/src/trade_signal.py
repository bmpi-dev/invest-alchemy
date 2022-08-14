from enum import Enum

class TradeSignalState(Enum):
    BUY = 'B' # buy
    SELL = 'S' # sell
    HOLD = 'H' # hold
    EMPTY = 'E' # empty
    ERROR = 'X' # error

class TradeSignal:
    """Trade signal base class"""

    def __init__(self, state, code, name):
        self.state = state
        self.code = code
        self.name = name

    def get_message(self):
        if self.state == TradeSignalState.BUY:
            return self.name + "(" + self.code + ")" + "可买, "
        elif self.state == TradeSignalState.SELL:
            return self.name + "(" + self.code + ")" + "可卖, "
        elif self.state == TradeSignalState.HOLD:
            return self.name + "(" + self.code + ")" + "持仓, "
        elif self.state == TradeSignalState.EMPTY:
            return self.name + "(" + self.code + ")" + "空仓, "
        return ''