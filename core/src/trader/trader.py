from abc import ABCMeta, abstractmethod
from typing import List

class ITrader(metaclass=ABCMeta):

    @abstractmethod
    def __init__(self, u_name=None):
        """Initialize the trader

        :param u_id: user id, store in the base.db
        :return: None
        """
        pass

    @abstractmethod
    def get_protfolios() -> List[str]:
        """Get the protfolios

        :return: the name list of the protfolios
        """
        pass

    @abstractmethod
    def update_protfolios(self, trade_date):
        """Update ledger data of trader's protfolios with given trade date

        :param trade_date: trade date
        :return: None
        """
        pass