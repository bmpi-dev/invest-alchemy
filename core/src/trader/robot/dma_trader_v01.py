from trader.trader import ITrader
from portfolio.trade_portfolio import Portfolio
from constants import TODAY_STR
from typing import List

def DMATraderV01(ITrader):
    """Robot trader(V01) who follow the Double MA strategy(MA parameter: 11/22)
       Note: One robot trader only can have one trade portfolio
    """

    def __init__(self, u_name=None):
        self.u_name = u_name if u_name else 'robot_dma_v01'
        self.__portfolios = [Portfolio(self.u_name, 'dma_11_22')]

    def portfolios() -> List[Portfolio]:
        return self.__portfolios

    def update_portfolios(self, trade_date):
        for p in self.portfolios:
            p.sync_files()
            self.__generate_transaction_with_strategy_signal(p, trade_date)
            self.__generate_funding_with_funding_strategy(p, trade_date)
            p.update_net_value_ledger(trade_date)
            p.sync_files()

    def __generate_transaction_with_strategy_signal(self, p: Portfolio, trade_date):
        """Generate transaction record with strategy (following the double MA strategy signals stored in base.db) by given trade date, only robot need do this

        :param trade_date: trade date
        :return: None
        """
        # TODO: implement
        pass

    def __generate_funding_with_funding_strategy(self, p: Portfolio, trade_date):
        """Generate funding record with funding strategy by given trade date, , only robot need do this

        :param trade_date: trade date
        :return: None
        """
        # TODO: implement
        pass