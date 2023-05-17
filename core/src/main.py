from storage import upload_file, connect_db, disconnect_db, get_premium_user_list
from constants import TRADE_DATE_FORMAT_STR, OUTPUT_FILE, S3_BUCKET_NAME, S3_DOUBLE_MA_BASE_DIR, TODAY_STR, MAX_STRATEGY_SIGNAL_ERROR_COUNT, LOCAL_BASE_DIR, STRATEGY_DMA_SHORT_TERM, STRATEGY_DMA_LONG_TERM, APP_ENV
from notification import send_email_smtp
from strategy.dma.dma_strategy import DMATradeStrategy
from message import generate_message_to_file
from db import DmaTradeSignalModel
from strategy.trade_signal import TradeSignalState
from client.ts_client import TSClient
from market.index_daily import IndexDaily
from os.path import exists
from datetime import datetime, timedelta
import os

from trader.robot.dma_trader_v01 import DMATraderV01
from trader.robot.dma_trader_v02 import DMATraderV02

def robot_trader_portfolio_cal():
    yesterday = datetime.strptime(TODAY_STR, TRADE_DATE_FORMAT_STR) - timedelta(1)
    yesterday_str = yesterday.strftime(TRADE_DATE_FORMAT_STR)

    trader1 = DMATraderV01()
    trader1.update_portfolios(yesterday_str)

    trader2 = DMATraderV02()
    trader2.update_portfolios(yesterday_str)

def startup():
    print('make sure local bash path exists...')
    if (not exists(LOCAL_BASE_DIR)):
        os.makedirs(LOCAL_BASE_DIR, exist_ok=True)

    print('connect db at startup...')
    connect_db()

def shutdown():
    print('disconnect db at shutdown...')
    disconnect_db()

def can_send_message():
    error_count = DmaTradeSignalModel.select().where(DmaTradeSignalModel.trade_date == TODAY_STR, DmaTradeSignalModel.trade_type == TradeSignalState.ERROR.value).count()
    if error_count >= MAX_STRATEGY_SIGNAL_ERROR_COUNT:
        print("Too many errors happened during get trade targets' price by tushare, stop sending message...")
        return False
    return APP_ENV == 'prod'

if __name__ == "__main__":
    startup()

    trade_data_client = TSClient()

    print('start sync index daily trade data...')
    IndexDaily(trade_data_client).process()

    print('start process long etf...')
    title_msg = '==Long ETF==\n'
    dma_strategy = DMATradeStrategy(trade_data_client, STRATEGY_DMA_SHORT_TERM, STRATEGY_DMA_LONG_TERM, TODAY_STR)
    dma_strategy.process("data/best_etf.txt")
    dma_strategy.save_signals_to_db()
    generate_message_to_file(dma_strategy, title_msg)

    print('start process other etf...')
    title_msg = '==Other ETF==\n'
    dma_strategy = DMATradeStrategy(trade_data_client, STRATEGY_DMA_SHORT_TERM, STRATEGY_DMA_LONG_TERM, TODAY_STR)
    dma_strategy.process("data/fund.txt")
    dma_strategy.save_signals_to_db()
    generate_message_to_file(dma_strategy, title_msg)
    
    if can_send_message():
        print('start upload output file to s3...')
        upload_file(LOCAL_BASE_DIR + OUTPUT_FILE, S3_BUCKET_NAME, S3_DOUBLE_MA_BASE_DIR + OUTPUT_FILE)
        print('end upload output file to s3')
        print('start send email...')
        with open(LOCAL_BASE_DIR + OUTPUT_FILE, 'r') as file:
            message = file.read()
            subject = '双均线策略交易信号: ' + TODAY_STR + ' - A股市场'
            premium_user_list = get_premium_user_list()
            for premium_user in premium_user_list:
                send_email_smtp(premium_user, subject, message)
        print('end send email')

    print('start process robot trader portfolio calculate...')
    robot_trader_portfolio_cal()

    shutdown()
