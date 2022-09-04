from trader.trader import ITrader
from portfolio.trade_portfolio import Portfolio
from portfolio.trade_portfolio import PortfolioType
from constants import TRADE_DATE_FORMAT_STR
from typing import List
from db import DmaTradeSignalModel
from trader.trader_util import *
from util.common import get_trade_qfq_price, get_trade_date_range
from strategy.trade_signal import TradeSignalState
import csv
import traceback

class DMATraderV02(ITrader):
    """Robot trader(V02) who follow the Double MA strategy(MA parameter: 11/22) but just trade `159915.SZ` target.
       Note: One robot trader only can have one trade portfolio
    """

    def __init__(self, u_name: str=None):
        self.u_name = u_name if u_name else 'robot_dma_v02'
        self.__portfolios = [Portfolio(self.u_name, 'dma_11_22', '20180920', portfolio_type=PortfolioType.PUBLIC.value)]
        self.__init_fund_amount_per_portfolio = 100000
        self.__max_amount_single_trade_target = 0 # no limit, all in
        self.__min_amount_single_trade_target = self.__init_fund_amount_per_portfolio / 100

    @property
    def portfolios(self) -> List[Portfolio]:
        return self.__portfolios

    def update_portfolios(self, trade_date):
        for p in self.portfolios:
            p.start()
            self.__generate_funding_with_funding_strategy(p, trade_date)
            self.__generate_transaction_with_strategy_signal(p, trade_date)
            p.update_net_value(trade_date)
            p.finish()

    def __get_trade_buy_price_amount_with_funding_strategy(self, p: Portfolio, trade_code, trade_date):
        current_available_amount = get_trade_amount_last_transaction_record(p.transaction_local_ledger, trade_code)
        if (current_available_amount is not None and current_available_amount > 0):
            raise Exception('already held position, abort to buy for portfolio(%s) of user(%s)' % (p.portfolio_name, p.u_name))
        _, current_available_funding = get_current_available_funding(p.funding_local_ledger)
        trade_price = get_trade_qfq_price(trade_date, trade_code)
        if (current_available_funding < self.__min_amount_single_trade_target):
            raise Exception('no enough funding, abort to buy for portfolio(%s) of user(%s)' % (p.portfolio_name, p.u_name))
        trade_amount = int(current_available_funding / trade_price / 100) * 100
        return trade_price, round(trade_amount, 3)

    def __generate_funding_with_funding_strategy(self, p: Portfolio, trade_date):
        """Generate funding record with funding strategy by given trade date, only robot need do this

        :param trade_date: trade date
        :return: None
        """
        print('generate_funding_with_funding_strategy for portfolio(%s) of user(%s)' % (p.portfolio_name, p.u_name))
        if (not exists(p.funding_local_ledger)):
            with open(p.funding_local_ledger, 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=FUNDING_LEDGER_CSV_HEADER)
                writer.writeheader()
            try:
                # only execute once
                update_funding_ledger({'trade_date': p.create_date, 'fund_amount': self.__init_fund_amount_per_portfolio, 'fund_type': 'in'}, p.funding_local_ledger, True)
            except Exception as e:
                print(e)

    def __generate_transaction_with_strategy_signal(self, p: Portfolio, trade_date):
        """Generate transaction record with strategy (following the double MA strategy signals stored in main database) by given trade date, only robot need do this

        :param trade_date: trade date
        :return: None
        """
        print('generate_transaction_with_strategy_signal for portfolio(%s) of user(%s)' % (p.portfolio_name, p.u_name))
        if (not exists(p.transaction_local_ledger)):
            with open(p.transaction_local_ledger, 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=TRANSACTION_LEDGER_CSV_HEADER)
                writer.writeheader()

        last_trade_date = get_last_trade_date(p)
        trade_dates = get_trade_date_range(last_trade_date, trade_date)
        if (len(trade_dates) < 1):
            print('portfolio(%s) of user(%s) no need to update, because no available trade days...' % (p.portfolio_name, p.u_name))
            return
        for trade_date in trade_dates:
            print('start process trade date(%s)...' % trade_date)
            buys = DmaTradeSignalModel.select().where(DmaTradeSignalModel.trade_date == trade_date, \
                                                      DmaTradeSignalModel.trade_type == TradeSignalState.BUY.value, \
                                                      DmaTradeSignalModel.trade_code == '159915.SZ')
            for buy in buys:
                print('start process buy signal, trade code(%s)...' % buy.trade_code)
                try:
                    code = buy.trade_code
                    name = buy.trade_name
                    trade_price, trade_amount = self.__get_trade_buy_price_amount_with_funding_strategy(p, code, trade_date)
                    update_funding_ledger({'trade_date': trade_date, 'fund_amount': -(trade_price * trade_amount), 'fund_type': 'buy'}, p.funding_local_ledger)
                    update_transaction_ledger({'trade_date': trade_date, 'trade_code': code, 'trade_name': name, 'trade_type': 'buy', 'trade_amount': trade_amount, 'trade_price': trade_price}, p.transaction_local_ledger)
                except Exception as e:
                    print(e)
                    # traceback.print_exc()
            
            sell_codes = DmaTradeSignalModel.select().where(DmaTradeSignalModel.trade_date == trade_date, \
                                                            DmaTradeSignalModel.trade_type == TradeSignalState.SELL.value, \
                                                            DmaTradeSignalModel.trade_code == '159915.SZ')
            for sell in sell_codes:
                print('start process sell signal, trade code(%s)...' % sell.trade_code)
                try:
                    code = sell.trade_code
                    name = sell.trade_name
                    trade_price, trade_amount = get_trade_sell_price_amount(p, code, trade_date)
                    if (trade_price is None or trade_amount is None):
                        continue
                    update_funding_ledger({'trade_date': trade_date, 'fund_amount': trade_price * trade_amount, 'fund_type': 'sell'}, p.funding_local_ledger)
                    update_transaction_ledger({'trade_date': trade_date, 'trade_code': code, 'trade_name': name, 'trade_type': 'sell', 'trade_amount': -(trade_amount), 'trade_price': trade_price}, p.transaction_local_ledger)
                except Exception as e:
                    print(e)
                    # traceback.print_exc()