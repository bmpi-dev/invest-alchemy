# execute this code when needs
import sys, os

sys.path.append(os.getcwd())

from trader.robot.dma_trader_v01 import DMATraderV01

trader = DMATraderV01()
trader.update_portfolios('20220820')