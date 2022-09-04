# execute this code when needs
import sys, os

sys.path.append(os.getcwd())

from trader.user_trader import UserTrader
from trader.trader import TraderStatus, TraderType
from portfolio.trade_portfolio import PortfolioType, PortfolioStatus
from db import PortfolioModel, TraderModel

TraderModel.insert(username='robot_dma_v01', trader_status=TraderStatus.NORMAL.value, trader_type=TraderType.ROBOT.value) \
                     .on_conflict(conflict_target=[TraderModel.username], \
                                       preserve=[TraderModel.trader_status, TraderModel.trader_type, TraderModel.update_timestamp]).execute()

PortfolioModel.insert(trader_username='robot_dma_v01', portfolio_name='dma_11_22', \
                      portfolio_create_date='20180920', portfolio_trade_date='20220801', \
                      portfolio_type=PortfolioType.PUBLIC.value, portfolio_status=PortfolioStatus.CREATE.value) \
                      .on_conflict(conflict_target=[PortfolioModel.trader_username, PortfolioModel.portfolio_name], \
                                   preserve=[PortfolioModel.portfolio_trade_date, PortfolioModel.portfolio_type, \
                                    PortfolioModel.portfolio_status, PortfolioModel.update_timestamp]).execute()

TraderModel.insert(username='robot_dma_v02', trader_status=TraderStatus.NORMAL.value, trader_type=TraderType.ROBOT.value) \
                     .on_conflict(conflict_target=[TraderModel.username], \
                                       preserve=[TraderModel.trader_status, TraderModel.trader_type, TraderModel.update_timestamp]).execute()

PortfolioModel.insert(trader_username='robot_dma_v02', portfolio_name='dma_11_22', \
                      portfolio_create_date='20180920', portfolio_trade_date='20220801', \
                      portfolio_type=PortfolioType.PUBLIC.value, portfolio_status=PortfolioStatus.CREATE.value) \
                      .on_conflict(conflict_target=[PortfolioModel.trader_username, PortfolioModel.portfolio_name], \
                                   preserve=[PortfolioModel.portfolio_trade_date, PortfolioModel.portfolio_type, \
                                    PortfolioModel.portfolio_status, PortfolioModel.update_timestamp]).execute()
