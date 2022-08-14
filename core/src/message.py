from email import message
import sys
from constants import OUTPUT_FILE
from strategy.trade_strategy import IStrategy
from strategy.trade_signal import TradeSignalState

class Logger(object):
    def __init__(self):
        self.terminal = sys.stdout
        self.log = open('/tmp/' + OUTPUT_FILE, "a")
        self.is_open = True

    def open(self):
        self.terminal = sys.stdout
        self.log = open('/tmp/' + OUTPUT_FILE, "a")
        self.is_open = True

    def close(self):
        self.log.close()
        self.is_open = False

    def write(self, message):
        self.terminal.write(message)
        if self.is_open:
            self.log.write(message)

    def flush(self):
        #this flush method is needed for python 3 compatibility.
        #this handles the flush command by doing nothing.
        #you might want to specify some extra behavior here.
        pass

def generate_message_to_file(strategy: IStrategy, title_msg: str) -> None:
    sys.stdout = Logger()

    buy_codes = []
    sell_codes = []
    hold_codes = []
    empty_codes = []

    for signal in strategy.trade_signals:
        state = signal.state
        code = signal.code
        name = signal.name
        message = signal.get_message()
        if state == TradeSignalState.BUY:
            buy_codes.append([code, name, message])
        elif state == TradeSignalState.SELL:
            sell_codes.append([code, name, message])
        elif state == TradeSignalState.HOLD:
            hold_codes.append([code, name, message])
        elif state == TradeSignalState.EMPTY:
            empty_codes.append([code, name, message])

    split_msg = '##########'

    print(title_msg)

    print('可买标的:')
    for _code, _name, message in buy_codes:
        print(message)
    
    print(split_msg)

    print('可卖标的:')
    for _code, _name, message in sell_codes:
        print(message)
    
    print(split_msg)

    print('持仓标的:')
    for _code, _name, message in hold_codes:
        print(message)

    print(split_msg)

    print('空仓标的:')
    for _code, _name, message in empty_codes:
        print(message)

    print('\n')
    
    sys.stdout.close()