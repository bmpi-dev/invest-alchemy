# execute this code when needs
import sys, os

sys.path.append(os.getcwd())

from trader.robot.dma_trader_v01 import DMATraderV01
from trader.robot.dma_trader_v02 import DMATraderV02

trader1 = DMATraderV01()
trader1.update_portfolios('20220820')

trader2 = DMATraderV02()
trader2.update_portfolios('20220820')