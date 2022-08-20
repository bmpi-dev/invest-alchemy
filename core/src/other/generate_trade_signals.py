# execute this code when needs

import sys, os
from datetime import datetime, timedelta

sys.path.append(os.getcwd())

from client.ts_client import TSClient
from constants import TODAY_STR, TRADE_DATE_FORMAT_STR, STRATEGY_DMA_SHORT_TERM, STRATEGY_DMA_LONG_TERM
from strategy.dma.dma_strategy import DMATradeStrategy

trade_data_client = TSClient()

trade_days = trade_data_client.get_a_share_trade_date((datetime.strptime(TODAY_STR, TRADE_DATE_FORMAT_STR) - timedelta(days=1000)).strftime(TRADE_DATE_FORMAT_STR), TODAY_STR)

for trade_date in trade_days:
    print('start process trade date %s...' % trade_date)
    dma_strategy = DMATradeStrategy(trade_data_client, STRATEGY_DMA_SHORT_TERM, STRATEGY_DMA_LONG_TERM, trade_date)
    dma_strategy.process("data/best_etf.txt")
    dma_strategy.save_signals_to_db()