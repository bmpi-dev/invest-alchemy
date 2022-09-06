# execute this code when needs
import sys, os
from datetime import datetime, timedelta

sys.path.append(os.getcwd())

from constants import TODAY_STR, TRADE_DATE_FORMAT_STR
from trader.robot.dma_trader_v01 import DMATraderV01
from trader.robot.dma_trader_v02 import DMATraderV02

def robot_trader_portfolio_cal():
    yesterday = datetime.strptime(TODAY_STR, TRADE_DATE_FORMAT_STR) - timedelta(1)
    yesterday_str = yesterday.strftime(TRADE_DATE_FORMAT_STR)

    trader1 = DMATraderV01()
    trader1.update_portfolios(yesterday_str)

    trader2 = DMATraderV02()
    trader2.update_portfolios(yesterday_str)

print('start process robot trader portfolio calculate...')
robot_trader_portfolio_cal()