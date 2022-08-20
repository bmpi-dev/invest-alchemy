from trader.trader import ITrader
from portfolio.trade_portfolio import Portfolio
from constants import TODAY_STR
from typing import List
from os.path import exists
import os
import csv

class DMATraderV01(ITrader):
    """Robot trader(V01) who follow the Double MA strategy(MA parameter: 11/22)
       Note: One robot trader only can have one trade portfolio
    """

    def __init__(self, u_name: str=None):
        self.u_name = u_name if u_name else 'robot_dma_v01'
        self.__portfolios = [Portfolio(self.u_name, 'dma_11_22')]

    @property
    def portfolios(self) -> List[Portfolio]:
        return self.__portfolios

    def update_portfolios(self, trade_date):
        for p in self.portfolios:
            p.start()
            self.__generate_funding_with_funding_strategy(p, trade_date)
            self.__generate_transaction_with_strategy_signal(p, trade_date)
            p.update_net_value_ledger(trade_date)
            p.finish()

    def __generate_funding_with_funding_strategy(self, p: Portfolio, trade_date):
        """Generate funding record with funding strategy by given trade date, only robot need do this

        :param trade_date: trade date
        :return: None
        """
        print('generate_funding_with_funding_strategy for portfolio(%s) of user(%s)' % (p.portfolio_name, p.u_name))
        if (not exists(p.funding_local_ledger)):
            with open(p.funding_local_ledger, 'w', newline='') as csvfile:
                fieldnames = ['trade_date', 'amount']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerow({'trade_date': '20180920', 'amount': 100000})


    def __generate_transaction_with_strategy_signal(self, p: Portfolio, trade_date):
        """Generate transaction record with strategy (following the double MA strategy signals stored in base.db) by given trade date, only robot need do this

        :param trade_date: trade date
        :return: None
        """
        print('generate_transaction_with_strategy_signal for portfolio(%s) of user(%s)' % (p.portfolio_name, p.u_name))
        if (not exists(p.transaction_local_ledger)):
            with open(p.funding_local_ledger, 'w', newline='') as csvfile:
                fieldnames = ['trade_date', 'trade_code', 'trade_name', 'trade_type', 'trade_amount', 'trade_price']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
        # TODO: implement
