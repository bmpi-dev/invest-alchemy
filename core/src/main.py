from storage import upload_file, sync_db, do_db_migration, disconnect_db, connect_db
from constants import OUTPUT_FILE, S3_BUCKET_NAME, S3_DOUBLE_MA_BASE_DIR, TODAY_STR
from notification import send_sns, send_tg_msg
from strategy import double_ma_strategy
from message import generate_message_to_file
from multiprocessing import Process
from db import DmaTradeSignal
from trade_signal import TradeSignalState

buy_codes = []
sell_codes = []
hold_codes = []
empty_codes = []

MAX_ERROR = 5

def reset_codes():
    buy_codes = []
    sell_codes = []
    hold_codes = []
    empty_codes = []

def process_codes(line):
    code_name = line.split(",")
    dma_trade_signal = double_ma_strategy(code_name[0], code_name[1].rstrip())
    state = dma_trade_signal.state
    code = dma_trade_signal.code
    name = dma_trade_signal.name
    message = dma_trade_signal.get_message()
    if state == TradeSignalState.BUY:
        buy_codes.append([code, name, message])
    elif state == TradeSignalState.SELL:
        sell_codes.append([code, name, message])
    elif state == TradeSignalState.HOLD:
        hold_codes.append([code, name, message])
    elif state == TradeSignalState.EMPTY:
        empty_codes.append([code, name, message])
    elif state == TradeSignalState.ERROR:
        print('Error happened for %s(%s), message is %s\n' % (name, code, message))
    DmaTradeSignal.insert(trade_date=TODAY_STR, trade_code=code, trade_name=name, trade_type=state.value).on_conflict_replace().execute()

def startup():
    print('sync db at startup...\n')
    sync_db()

    print('\nstart migrate db in a new process...\n')
    p = Process(target=do_db_migration, args=())
    p.start()
    p.join(timeout=60)

    if p.is_alive():
        print('do db migration timeout error...\n')
    else:
        print('done db migration')

    print('connect db at startup...\n')
    connect_db()

def shutdown():
    print('sync db at shutdown...\n')
    sync_db()
    print('disconnect db at shutdown...\n')
    disconnect_db()

def can_send_message():
    error_count = DmaTradeSignal.select().where(DmaTradeSignal.trade_date == TODAY_STR, DmaTradeSignal.trade_type == TradeSignalState.ERROR.value).count()
    if error_count >= MAX_ERROR:
        print("Too many errors happened during get trade targets' price by tushare, stop sending message...\n")
        return False
    return True

if __name__ == "__main__":
    startup()

    print('start process long etf...\n')
    title_msg = '==Long ETF==\n'
    with open("data/best_etf.txt", "r") as f:
        for line in f:
            process_codes(line)
    generate_message_to_file(buy_codes, sell_codes, hold_codes, empty_codes, title_msg)

    reset_codes()

    print('start process other etf...\n')
    title_msg = '==Other ETF==\n'
    with open("data/fund.txt", "r") as f:
        for line in f:
            process_codes(line)
    generate_message_to_file(buy_codes, sell_codes, hold_codes, empty_codes, title_msg)
    
    if can_send_message():
        print('\nstart upload output file to s3...\n')
        upload_file('/tmp/' + OUTPUT_FILE, S3_BUCKET_NAME, S3_DOUBLE_MA_BASE_DIR + OUTPUT_FILE)
        print('end upload output file to s3\n')
        print('start send sns...\n')
        send_sns('/tmp/' + OUTPUT_FILE)
        print('end send sns...\n')
        print('start send tg msg...\n')
        send_tg_msg('/tmp/' + OUTPUT_FILE)
        print('end send tg msg...\n')

    shutdown()
