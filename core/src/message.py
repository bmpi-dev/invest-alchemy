from email import message
import sys
from constants import OUTPUT_FILE

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

def generate_message_to_file(buy_codes, sell_codes, hold_codes, empty_codes, title_msg):
    sys.stdout = Logger()

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