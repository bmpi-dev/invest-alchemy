from abc import ABCMeta, abstractmethod, abstractproperty
from typing import List
from portfolio.trade_portfolio import Portfolio
from enum import Enum

class TraderStatus(Enum):
    NORMAL = 'N'
    DISABLE = 'D'

class TraderType(Enum):
    COMMON = 'C' # common user trader
    ROBOT = 'R' # robot trader

class ITrader(metaclass=ABCMeta):
    @abstractproperty
    def portfolios(self) -> List[Portfolio]:
        """Get the portfolios

        :return: the list of the Portfolio
        """
        pass

    @abstractmethod
    def __init__(self, u_name: str=None):
        """Initialize the trader

        :param u_id: user id, store in the base.db
        :return: None
        """
        pass

    @abstractmethod
    def update_portfolios(self, trade_date):
        """Update ledger data of trader's portfolios with given trade date

        :param trade_date: trade date
        :return: None
        """
        pass