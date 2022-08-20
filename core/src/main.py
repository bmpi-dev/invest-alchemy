from storage import upload_file, sync_db, do_db_migration, disconnect_db, connect_db
from constants import OUTPUT_FILE, S3_BUCKET_NAME, S3_DOUBLE_MA_BASE_DIR, TODAY_STR, MAX_STRATEGY_SIGNAL_ERROR_COUNT, LOCAL_BASE_DIR, STRATEGY_DMA_SHORT_TERM, STRATEGY_DMA_LONG_TERM
from notification import send_sns, send_tg_msg
from strategy.dma.dma_strategy import DMATradeStrategy
from message import generate_message_to_file
from multiprocessing import Process
from db import DmaTradeSignalModel
from strategy.trade_signal import TradeSignalState
from client.ts_client import TSClient

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
    error_count = DmaTradeSignalModel.select().where(DmaTradeSignalModel.trade_date == TODAY_STR, DmaTradeSignalModel.trade_type == TradeSignalState.ERROR.value).count()
    if error_count >= MAX_STRATEGY_SIGNAL_ERROR_COUNT:
        print("Too many errors happened during get trade targets' price by tushare, stop sending message...\n")
        return False
    return False # TODO: - check when deploy to production

if __name__ == "__main__":
    startup()

    trade_data_client = TSClient()

    print('start process long etf...\n')
    title_msg = '==Long ETF==\n'
    dma_strategy = DMATradeStrategy(trade_data_client, STRATEGY_DMA_SHORT_TERM, STRATEGY_DMA_LONG_TERM, TODAY_STR)
    dma_strategy.process("data/best_etf.txt")
    dma_strategy.save_signals_to_db()
    generate_message_to_file(dma_strategy, title_msg)

    print('start process other etf...\n')
    title_msg = '==Other ETF==\n'
    dma_strategy = DMATradeStrategy(trade_data_client, STRATEGY_DMA_SHORT_TERM, STRATEGY_DMA_LONG_TERM, TODAY_STR)
    dma_strategy.process("data/fund.txt")
    dma_strategy.save_signals_to_db()
    generate_message_to_file(dma_strategy, title_msg)
    
    if can_send_message():
        print('\nstart upload output file to s3...\n')
        upload_file(LOCAL_BASE_DIR + OUTPUT_FILE, S3_BUCKET_NAME, S3_DOUBLE_MA_BASE_DIR + OUTPUT_FILE)
        print('end upload output file to s3\n')
        print('start send sns...\n')
        send_sns(LOCAL_BASE_DIR + OUTPUT_FILE)
        print('end send sns...\n')
        print('start send tg msg...\n')
        send_tg_msg(LOCAL_BASE_DIR + OUTPUT_FILE)
        print('end send tg msg...\n')

    shutdown()
