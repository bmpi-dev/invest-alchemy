# execute this code when needs
import sys, os

sys.path.append(os.getcwd())

from trader.user_trader import UserTrader
from trader.trader import TraderStatus, TraderType
from portfolio.trade_portfolio import PortfolioType, PortfolioStatus
from db import PortfolioModel, TraderModel

TraderModel.insert(username='bmpi', trader_status=TraderStatus.NORMAL.value, trader_type=TraderType.COMMON.value) \
                     .on_conflict(conflict_target=[TraderModel.username], \
                                       preserve=[TraderModel.trader_status, TraderModel.trader_type, TraderModel.update_timestamp]).execute()

PortfolioModel.insert(trader_username='bmpi', portfolio_name='被动收入', \
                      portfolio_create_date='20180801', portfolio_trade_date='20230513', \
                      portfolio_type=PortfolioType.PUBLIC.value, portfolio_status=PortfolioStatus.CREATE.value) \
                      .on_conflict(conflict_target=[PortfolioModel.trader_username, PortfolioModel.portfolio_name], \
                                   preserve=[PortfolioModel.portfolio_trade_date, PortfolioModel.portfolio_type, \
                                    PortfolioModel.portfolio_status, PortfolioModel.update_timestamp]).execute()

bmpi = UserTrader('bmpi')
bmpi.update_portfolios('20230513')