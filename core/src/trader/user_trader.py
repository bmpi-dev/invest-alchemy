from trader.trader import ITrader, TraderType, TraderStatus
from portfolio.trade_portfolio import Portfolio
from constants import TRADE_DATE_FORMAT_STR
from typing import List
from db import TraderModel, PortfolioModel, DoesNotExist
from trader.trader_util import FUNDING_LEDGER_CSV_HEADER, TRANSACTION_LEDGER_CSV_HEADER
from portfolio.trade_portfolio import PortfolioType, PortfolioStatus
from util.common import is_trader_robot
from os.path import exists
import csv
import traceback

class UserTrader(ITrader):
    """User trader class for supporting to calculate user's portfolio.
       Note: Currently user trader's portfolio calculation is triggered by manually while robot trader is automatically, because user's transaction/funding ledger data may not be available when calculate the portfolio net value.
    """

    def __init__(self, u_name: str=None):
        try:
            trader = TraderModel.select().where(TraderModel.username == u_name, \
                                                TraderModel.trader_status == TraderStatus.NORMAL.value, \
                                                TraderModel.trader_type == TraderType.COMMON.value).get()
        except DoesNotExist:
            raise Exception('trader can not find in database, or status is not normal, or trader type is not user, abort init...')
        if (is_trader_robot(u_name)):
            raise Exception('user trader name can not start with robot_, abort init...')
        self.u_name = u_name
        self.__portfolios = None
        self.__trader = trader

    @property
    def portfolios(self) -> List[Portfolio]:
        if (self.__portfolios is None):
            portfolios_db =  PortfolioModel.select().where(PortfolioModel.trader_username == self.u_name, \
                                                               PortfolioModel.portfolio_status != PortfolioStatus.STOP.value, \
                                                               PortfolioModel.portfolio_status != PortfolioStatus.DISABLE.value)
            portfolios = []
            for p in portfolios_db:
                portfolios.append(Portfolio(self.u_name, p.portfolio_name, p.portfolio_create_date))
            self.__portfolios = portfolios
        return self.__portfolios

    def update_portfolios(self, trade_date):
        for p in self.portfolios:
            p.start()
            self.__ensure_trader_basic_ledger_exists(p)
            p.update_net_value(trade_date)
            p.finish()

    def __ensure_trader_basic_ledger_exists(self, p: Portfolio):
        if (not exists(p.funding_local_ledger)):
            with open(p.funding_local_ledger, 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=FUNDING_LEDGER_CSV_HEADER)
                writer.writeheader()
        if (not exists(p.transaction_local_ledger)):
            with open(p.transaction_local_ledger, 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=TRANSACTION_LEDGER_CSV_HEADER)
                writer.writeheader()