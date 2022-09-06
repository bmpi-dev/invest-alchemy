from trader.trader import ITrader
from portfolio.trade_portfolio import Portfolio
from portfolio.trade_portfolio import PortfolioType
from constants import TRADE_DATE_FORMAT_STR
from typing import List
from db import DmaTradeSignalModel
from trader.trader_util import *
from util.common import get_trade_close_price, get_trade_date_range, get_the_day_after_n, get_the_day_before_n, get_qfq_close_price
from strategy.trade_signal import TradeSignalState
import csv
import traceback

class DMATraderV01(ITrader):
    """Robot trader(V01) who follow the Double MA strategy(MA parameter: 11/22)
       Note: One robot trader only can have one trade portfolio
    """

    def __init__(self, u_name: str=None):
        self.u_name = u_name if u_name else 'robot_dma_v01'
        self.__portfolios = [Portfolio(self.u_name, 'dma_11_22', '20180920', portfolio_type=PortfolioType.PUBLIC.value)]
        self.__init_fund_amount_per_portfolio = 100000
        self.__max_amount_single_trade_target = self.__init_fund_amount_per_portfolio / 5 # single trade target can only buy 1/5 of the funding
        self.__min_amount_single_trade_target = self.__init_fund_amount_per_portfolio / 20

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
        trade_price = get_trade_close_price(trade_date, trade_code)
        if (current_available_funding < self.__min_amount_single_trade_target):
            raise Exception('no enough funding, abort to buy for portfolio(%s) of user(%s)' % (p.portfolio_name, p.u_name))
        if (current_available_funding > self.__max_amount_single_trade_target):
            trade_amount = int(self.__max_amount_single_trade_target / trade_price / 100) * 100 # rounding to the nearest hundred because minimum tradeable quantity is a multiple of one hundred
        else:
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
        trade_dates = get_trade_date_range(get_the_day_after_n(last_trade_date, 1), trade_date)
        if (len(trade_dates) < 1):
            print('portfolio(%s) of user(%s) no need to update, because no available trade days...' % (p.portfolio_name, p.u_name))
            return
        
        current_holdings = get_current_holdings(p.transaction_local_ledger)

        for trade_date in trade_dates:
            print('start process trade date(%s)...' % trade_date)
            for code in current_holdings.keys():
                if current_holdings[code][0] > 1:
                    price_data = get_qfq_close_price(code, get_the_day_before_n(trade_date, 15), trade_date)
                    adj_factor = float(price_data['adj_factor'].iloc[-1] / price_data['adj_factor'].iloc[-2])
                    if (adj_factor != 1.0):
                        print('process split-adjusted share prices case: holding code(%s) with trade date(%s), found adj_factor(%d) for portfolio(%s) of user(%s)' % (code, trade_date, adj_factor, p.portfolio_name, p.u_name))
                        change_amount = current_holdings[code][0] * adj_factor - current_holdings[code][0]
                        current_holdings[code][0] = round(current_holdings[code][0] * adj_factor, 3)
                        update_transaction_ledger({'trade_date': trade_date, 'trade_code': code, 'trade_name': current_holdings[code][1], 'trade_type': 'buy' if change_amount > 0 else 'sell', 'trade_amount': change_amount, 'trade_price': 0.000001}, p.transaction_local_ledger)
            
            buys = DmaTradeSignalModel.select().where(DmaTradeSignalModel.trade_date == trade_date, DmaTradeSignalModel.trade_type == TradeSignalState.BUY.value)
            for buy in buys:
                print('start process buy signal, trade code(%s)...' % buy.trade_code)
                try:
                    code = buy.trade_code
                    name = buy.trade_name
                    trade_price, trade_amount = self.__get_trade_buy_price_amount_with_funding_strategy(p, code, trade_date)
                    update_funding_ledger({'trade_date': trade_date, 'fund_amount': -(trade_price * trade_amount), 'fund_type': 'buy'}, p.funding_local_ledger)
                    update_transaction_ledger({'trade_date': trade_date, 'trade_code': code, 'trade_name': name, 'trade_type': 'buy', 'trade_amount': trade_amount, 'trade_price': trade_price}, p.transaction_local_ledger)
                    if (code in current_holdings):
                        current_holdings[code][0] = current_holdings[code][0] + trade_amount
                    else:
                        current_holdings[code][0] = trade_amount
                except Exception as e:
                    print(e)
                    # traceback.print_exc()
            sell_codes = DmaTradeSignalModel.select().where(DmaTradeSignalModel.trade_date == trade_date, DmaTradeSignalModel.trade_type == TradeSignalState.SELL.value)
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
                    if (code in current_holdings):
                        current_holdings[code][0] = current_holdings[code][0] - trade_amount
                    else:
                        raise Exception('!!!no holding to sell(code: %s) for portfolio(%s) of user(%s)!!!' % (code, p.portfolio_name, p.u_name))
                except Exception as e:
                    print(e)
                    # traceback.print_exc()