# execute this code when needs
import sys, os

sys.path.append(os.getcwd())

from trader.trader_util import get_current_holdings

print(get_current_holdings('/tmp/invest-alchemy/portfolio/robot_dma_v01/dma_11_22/transaction_ledger.csv'))
