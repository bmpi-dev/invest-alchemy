from constants import LOCAL_BASE_DIR, S3_PORTFOLIO_BASE_DIR
from os.path import exists
from storage import s3_client
import botocore
from constants import S3_BUCKET_NAME
import os, sys, csv
from portfolio.portfolio_db import *
from util.common import *
from datetime import datetime, timedelta
from constants import TRADE_DATE_FORMAT_STR
from util.common import get_trade_close_price, get_qfq_close_price, CAGR, SHARPE_RATIO, is_trader_robot
import pandas as pd
from enum import Enum

class PortfolioStatus(Enum):
    CREATE = 'C'
    RUNNING = 'R'
    STOP = 'S'
    DISABLE = 'D'

class PortfolioType(Enum):
    PRIVATE = 'private'
    PUBLIC = 'public'

class Portfolio:
    """Trade Portfolio class"""

    def __init__(self, u_name, portfolio_name, create_date, portfolio_type=PortfolioType.PRIVATE.value):
        self.u_name = u_name
        self.portfolio_name = portfolio_name
        self.create_date = create_date
        self.portfolio_local_base_path = LOCAL_BASE_DIR + 'portfolio/' + self.u_name + '/' + self.portfolio_name + '/'
        self.portfolio_remote_base_path = S3_PORTFOLIO_BASE_DIR + self.u_name + '/' + self.portfolio_name + '/'
        self.portfolio_db_local_path = self.portfolio_local_base_path + self.portfolio_name + '.db'
        self.portfolio_db_remote_path = self.portfolio_remote_base_path + self.portfolio_name + '.db'
        self.transaction_local_ledger = self.portfolio_local_base_path + 'transaction_ledger.csv'
        self.transaction_remote_ledger = self.portfolio_remote_base_path + 'transaction_ledger.csv'
        self.funding_local_ledger = self.portfolio_local_base_path + 'funding_ledger.csv'
        self.funding_remote_ledger = self.portfolio_remote_base_path + 'funding_ledger.csv'
        self.portfolio_type = portfolio_type

    def __init_work_dir(self):
        if (exists(self.portfolio_db_local_path)):
            print('delete local files for portfolio(%s) of user(%s)' % (self.portfolio_name, self.u_name))
            try:
                os.remove(self.portfolio_db_local_path)
                os.remove(self.transaction_local_ledger)
                os.remove(self.funding_local_ledger)
            except Exception as e:
                print(e)
        else:
            os.makedirs(self.portfolio_local_base_path, exist_ok=True)

    def start(self):
        print('====> start to process portfolio(%s) for user(%s) <====' % (self.portfolio_name, self.u_name))
        self.__init_work_dir()
        print('download the files from s3 to local for portfolio(%s) of user(%s)' % (self.portfolio_name, self.u_name))
        try:
            s3_client.download_file(S3_BUCKET_NAME, self.portfolio_db_remote_path, self.portfolio_db_local_path)
            s3_client.download_file(S3_BUCKET_NAME, self.transaction_remote_ledger, self.transaction_local_ledger)
            s3_client.download_file(S3_BUCKET_NAME, self.funding_remote_ledger, self.funding_local_ledger)
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                print('not found this portfolio(%s) data for user(%s), create base path in local...' % (self.portfolio_name, self.u_name))
                os.makedirs(os.path.dirname(self.portfolio_local_base_path), exist_ok=True)
            else:
                print(e)
        print('start connect database for portfolio(%s) ot user(%s)' % (self.portfolio_name, self.u_name))
        re_bind_db(self.portfolio_db_local_path)

    def finish(self):
        if (exists(self.portfolio_db_local_path)):
            print('start disconnect database for portfolio(%s) ot user(%s)' % (self.portfolio_name, self.u_name))
            disconnect_db()
            print('upload the files to s3 for portfolio(%s) of user(%s)' % (self.portfolio_name, self.u_name))
            db_s3_flag = {'ACL': 'public-read'} if self.portfolio_type == PortfolioType.PUBLIC.value else {}
            s3_client.upload_file(self.portfolio_db_local_path, S3_BUCKET_NAME, self.portfolio_db_remote_path, ExtraArgs=db_s3_flag)
            s3_client.upload_file(self.transaction_local_ledger, S3_BUCKET_NAME, self.transaction_remote_ledger)
            s3_client.upload_file(self.funding_local_ledger, S3_BUCKET_NAME, self.funding_remote_ledger)
        else:
            print('not found this portfolio(%s) data for user(%s), maybe something wrong happened...' % (self.portfolio_name, self.u_name))
        print('====> finish to process portfolio(%s) for user(%s) <====' % (self.portfolio_name, self.u_name))

    def __update_transaction_ledger(self, trade_date):
        """Update transaction ledger on the given trade date

        :param trade_date: trade date
        :return: None
        """
        try:
            last_record_db = TransactionLedgerModel.select().order_by(TransactionLedgerModel.trade_date.desc()).get()
            last_trade_date_db = last_record_db.trade_date
        except DoesNotExist:
            # fix missing record if first funding transcation happened on the create date of the portfolio, because it uses trade_date_big function to determin if the funding ledger needs to update
            the_day_before_portfolio_create = datetime.strptime(self.create_date, TRADE_DATE_FORMAT_STR) - timedelta(1)
            last_trade_date_db = the_day_before_portfolio_create.strftime(TRADE_DATE_FORMAT_STR)
        with open(self.transaction_local_ledger, 'r', newline='') as csvfile:
            rows = csv.DictReader(csvfile)
            for row in rows:
                trade_date_csv = row['trade_date']
                if (trade_date_big(trade_date_csv, last_trade_date_db)):
                    print('update transaction ledger of portfolio(%s) for user(%s), trade date: %s...' % (self.portfolio_name, self.u_name, trade_date_csv))
                    trade_type = row['trade_type'].lower()
                    if (trade_type == 'buy'):
                        trade_amount = abs(round(float(row['trade_amount']), 3)) # plus meaning buy
                    else:
                        trade_amount = -1 * abs(round(float(row['trade_amount']), 3)) # minus meaning sell
                    trade_price=round(float(row['trade_price']), 3)
                    trade_money=round(trade_amount * trade_price, 3)
                    current_available_amount=round(float(0 if row['current_available_amount']=='' else row['current_available_amount']), 3)
                    save_db = TransactionLedgerModel(trade_date=trade_date_csv, \
                                                    trade_code=row['trade_code'], \
                                                    trade_name=row['trade_name'], \
                                                    trade_type=trade_type, \
                                                    trade_amount=trade_amount, \
                                                    current_available_amount=current_available_amount, \
                                                    trade_price=trade_price, \
                                                    trade_money=trade_money, \
                                                    handling_fees=0.0, \
                                                    funding_percentage=0.0)
                    save_db.save()

    def __update_funding_ledger(self, trade_date):
        """Update funding ledger on the given trade date

        :param trade_date: trade date
        :return: None
        """
        try:
            last_record_db = FundingLedgerModel.select().order_by(FundingLedgerModel.trade_date.desc()).get()
            last_trade_date_db = last_record_db.trade_date
        except DoesNotExist:
            # fix missing record if first funding transcation happened on the create date of the portfolio, because it uses trade_date_big function to determin if the funding ledger needs to update
            the_day_before_portfolio_create = datetime.strptime(self.create_date, TRADE_DATE_FORMAT_STR) - timedelta(1)
            last_trade_date_db = the_day_before_portfolio_create.strftime(TRADE_DATE_FORMAT_STR)
        with open(self.funding_local_ledger, 'r', newline='') as csvfile:
            rows = csv.DictReader(csvfile)
            for row in rows:
                trade_date_csv = row['trade_date']
                if (trade_date_big(trade_date_csv, last_trade_date_db)):
                    print('update funding ledger of portfolio(%s) for user(%s), trade date: %s...' % (self.portfolio_name, self.u_name, trade_date_csv))
                    fund_type = row['fund_type'].lower()
                    if (fund_type == 'in'):
                        fund_amount = abs(round(float(row['fund_amount']), 3)) # plus meaning in
                    else:
                        fund_amount = -1 * abs(round(float(row['fund_amount']), 3)) # minus meaning out
                    current_available_amount=round(float(0 if row['current_available_amount']=='' else row['current_available_amount']), 3)
                    save_db = FundingLedgerModel(trade_date=trade_date_csv, \
                                                fund_amount=fund_amount, \
                                                current_available_amount=current_available_amount, \
                                                fund_type=fund_type)
                    save_db.save()

    def __update_holding_ledger(self, trade_date):
        """Update holding ledger on the given trade date

        :param trade_date: trade date
        :return: None
        """
        last_trade_date_db = self.create_date
        try:
            last_record_db = HoldingLedgerModel.select().order_by(HoldingLedgerModel.trade_date.desc()).get()
            last_trade_date_db = last_record_db.trade_date
        except DoesNotExist:
            # init holding ledger with first transaction records
            print('no holding, init it with first transaction records')
            try:
                first_transaction = TransactionLedgerModel.select().order_by(TransactionLedgerModel.trade_date.asc()).get()
                first_transaction_date = first_transaction.trade_date
                first_transactions = TransactionLedgerModel.select().where(TransactionLedgerModel.trade_date == first_transaction_date)
                for transaction in first_transactions:
                    if (transaction.trade_amount > 0):
                        close_price = get_trade_close_price(first_transaction_date, transaction.trade_code)
                        market_value = transaction.trade_amount * close_price
                        HoldingLedgerModel.insert(trade_date=first_transaction_date, \
                                                  trade_code=transaction.trade_code, \
                                                  trade_name=transaction.trade_name, \
                                                  hold_amount=transaction.trade_amount, \
                                                  close_price=close_price, \
                                                  market_value=market_value, \
                                                  position_percentage=0.0).on_conflict_replace().execute()
                last_trade_date_db = first_transaction_date
            except DoesNotExist:
                return
        
        day_before_start_date = datetime.strptime(last_trade_date_db, TRADE_DATE_FORMAT_STR)
        start_date = day_before_start_date + timedelta(1)
        end_date = datetime.strptime(trade_date, TRADE_DATE_FORMAT_STR)
        days = (end_date - day_before_start_date).days

        if (days <= 0):
            return
        
        for i in range(days):
            _trade_date = start_date + timedelta(i)
            _day_before_trade_date_str = (_trade_date - timedelta(1)).strftime(TRADE_DATE_FORMAT_STR)
            _trade_date_str = _trade_date.strftime(TRADE_DATE_FORMAT_STR)

            print('update holding ledger of portfolio(%s) for user(%s), trade date: %s...' % (self.portfolio_name, self.u_name, _trade_date_str))

            last_holdings = HoldingLedgerModel.select().where(HoldingLedgerModel.trade_date == _day_before_trade_date_str)
            transaction_records = TransactionLedgerModel.select().where(TransactionLedgerModel.trade_date == _trade_date_str)
            # calculate current holdings postion
            current_holds = []
            for holding in last_holdings:
                print('holding: %s' % holding.trade_code)
                current_holds.append(HoldingLedgerModel(trade_date=_trade_date_str, \
                                                        trade_code=holding.trade_code, \
                                                        trade_name=holding.trade_name, \
                                                        hold_amount=holding.hold_amount, \
                                                        close_price=holding.close_price, \
                                                        market_value=holding.market_value, \
                                                        position_percentage=0.0))
            for transaction in transaction_records:
                print('transaction db id: %d, code: %s, trade type: %s' % (transaction.id, transaction.trade_code, transaction.trade_type))
                is_new = True
                for holding in current_holds:
                    if (transaction.trade_code == holding.trade_code):
                        holding.hold_amount = holding.hold_amount + transaction.trade_amount
                        is_new = False
                if (is_new):
                    if (transaction.trade_amount > 0):
                        current_holds.append(HoldingLedgerModel(trade_date=_trade_date_str, \
                                                                trade_code=transaction.trade_code, \
                                                                trade_name=transaction.trade_name, \
                                                                hold_amount=transaction.trade_amount, \
                                                                close_price=transaction.trade_price, \
                                                                market_value=transaction.trade_money, \
                                                                position_percentage=0.0))
                    else:
                        raise Exception('process holding ledger error for portfolio(%s) of user(%s), because no holding but have a sell transaction record(DB id is %s)!' % (self.portfolio_name, self.u_name, transaction))
            
            for hold in current_holds:
                try:
                    # it musts get 15 days price data for calculating the split-adjusted share prices, because TSClient can not give data on non-trading date, so we need get price data on the trade day before the current trade day, 15 days is enough for A share stock.
                    price_data = get_qfq_close_price(hold.trade_code, (_trade_date - timedelta(15)).strftime(TRADE_DATE_FORMAT_STR), _trade_date_str)
                    close_price = round(float(price_data['close'].iloc[-1]), 3)
                    hold.close_price = close_price
                    hold.market_value = round(hold.close_price * hold.hold_amount, 3)
                    adj_factor = float(price_data['adj_factor'].iloc[-1] / price_data['adj_factor'].iloc[-2])
                    # only robot trader need process split-adjusted case
                    if (is_trader_robot(self.u_name)):
                        if (adj_factor != 1.0):
                            print('process split-adjusted share prices case: holding code(%s) with trade date(%s), found adj_factor(%d) for portfolio(%s) of user(%s)' % (hold.trade_code, _trade_date_str, adj_factor, self.portfolio_name, self.u_name))
                            hold.hold_amount = round(hold.hold_amount * adj_factor, 3)
                            hold.market_value = round(hold.close_price * hold.hold_amount, 3)
                except Exception as e:
                    print('Exception: %s' % e)
                # ignore hold amount less than 1 for excluding calculation fragments
                if (hold.hold_amount <= 1):
                    print('remove hold: %s' % hold.trade_code)
                else:
                    HoldingLedgerModel.insert(trade_date=hold.trade_date, \
                                              trade_code=hold.trade_code, \
                                              trade_name=hold.trade_name, \
                                              hold_amount=hold.hold_amount, \
                                              close_price=hold.close_price, \
                                              market_value=hold.market_value, \
                                              position_percentage=hold.position_percentage).on_conflict_replace().execute()

    def __update_net_value_ledger(self, trade_date):
        """Update portfolio net value ledger on the given trade date

        :param trade_date: trade date
        :return: None
        """
        the_day_before_portfolio_create = datetime.strptime(self.create_date, TRADE_DATE_FORMAT_STR) - timedelta(1)
        last_trade_date_db = the_day_before_portfolio_create.strftime(TRADE_DATE_FORMAT_STR)
        try:
            last_record_db = NetValueLedgerModel.select().order_by(NetValueLedgerModel.trade_date.desc()).get()
            last_trade_date_db = last_record_db.trade_date
        except DoesNotExist:
            print('no net value, init it...')
            NetValueLedgerModel.insert(trade_date=last_trade_date_db, \
                                       net_value=1.0, \
                                       total_shares=0.0, \
                                       total_assets=0.0, \
                                       hold_assets=0.0, \
                                       fund_balance=0.0).on_conflict_replace().execute()

        day_before_start_date = datetime.strptime(last_trade_date_db, TRADE_DATE_FORMAT_STR)
        start_date = day_before_start_date + timedelta(1)
        end_date = datetime.strptime(trade_date, TRADE_DATE_FORMAT_STR)
        days = (end_date - day_before_start_date).days

        if (days <= 0):
            return
        
        for i in range(days):
            try:
                _trade_date = start_date + timedelta(i)
                _day_before_trade_date_str = (_trade_date - timedelta(1)).strftime(TRADE_DATE_FORMAT_STR)
                _trade_date_str = _trade_date.strftime(TRADE_DATE_FORMAT_STR)

                print('calculate net value ledger for portfolio(%s) of user(%s), trade date is %s' % (self.portfolio_name, self.u_name, _trade_date_str))

                last_net_value = NetValueLedgerModel.select().where(NetValueLedgerModel.trade_date == _day_before_trade_date_str).get()
                current_fundings = FundingLedgerModel.select().where(FundingLedgerModel.trade_date == _trade_date_str)
                current_transactions = TransactionLedgerModel.select().where(TransactionLedgerModel.trade_date == _trade_date_str)
                funding_change = 0.0
                trade_money_change = 0.0
                for funding in current_fundings:
                    if (funding.fund_type == 'in' or funding.fund_type == 'out'):
                        funding_change = funding_change + funding.fund_amount
                for transaction in current_transactions:
                    if (transaction.trade_type == 'buy' or transaction.trade_type == 'sell'):
                        trade_money_change = trade_money_change - transaction.trade_money # minus trade_money meaning sell, plus meaning buy
                
                shares_change = round(funding_change / last_net_value.net_value, 3)

                current_hold_assets = 0.0
                current_holds = HoldingLedgerModel.select().where(HoldingLedgerModel.trade_date == _trade_date_str)
                for hold in current_holds:
                    current_hold_assets = current_hold_assets + hold.market_value

                current_total_shares = last_net_value.total_shares + shares_change
                current_fund_balance = round(last_net_value.fund_balance + funding_change + trade_money_change, 3)
                current_total_assets = round(current_hold_assets + current_fund_balance, 3)
                current_net_value = 1.0 if current_total_shares == 0 else round(current_total_assets / current_total_shares, 3)
                
                NetValueLedgerModel.insert(trade_date=_trade_date_str, \
                                        net_value=current_net_value, \
                                        total_shares=current_total_shares, \
                                        total_assets=current_total_assets, \
                                        hold_assets=current_hold_assets, \
                                        fund_balance=current_fund_balance).on_conflict_replace().execute()
            except Exception as e:
                print('Exception: %s' % e)
    
    def __update_performance_ledger(self, trade_date):
        """Update portfolio performance ledger on the given trade date

        :param trade_date: trade date
        :return: None
        """
        the_day_before_portfolio_create = datetime.strptime(self.create_date, TRADE_DATE_FORMAT_STR) - timedelta(1)
        last_trade_date_db = the_day_before_portfolio_create.strftime(TRADE_DATE_FORMAT_STR)
        try:
            last_record_db = PerformanceLedgerModel.select().order_by(PerformanceLedgerModel.trade_date.desc()).get()
            last_trade_date_db = last_record_db.trade_date
        except DoesNotExist:
            print('no performance record, init it...')
            PerformanceLedgerModel.insert(trade_date=last_trade_date_db, \
                                        change_percentage=0.0, \
                                        retracement_range=0.0, \
                                        max_retracement_range=0.0, \
                                        days_of_continuous_loss=1.0, \
                                        max_days_of_continuous_loss=0, \
                                        days_of_win=0, \
                                        days_of_loss=0, \
                                        run_days=0, \
                                        total_trade_count=0, \
                                        cagr=0.0, \
                                        sharpe_ratio=0.0, \
                                        hold_risk_count=0, \
                                        buy_risk_count=0).on_conflict_replace().execute()

        day_before_start_date = datetime.strptime(last_trade_date_db, TRADE_DATE_FORMAT_STR)
        start_date = day_before_start_date + timedelta(1)
        end_date = datetime.strptime(trade_date, TRADE_DATE_FORMAT_STR)
        days = (end_date - day_before_start_date).days

        if (days <= 0):
            return
        
        for i in range(days):
            try:
                _trade_date = start_date + timedelta(i)
                _day_before_trade_date_str = (_trade_date - timedelta(1)).strftime(TRADE_DATE_FORMAT_STR)
                _trade_date_str = _trade_date.strftime(TRADE_DATE_FORMAT_STR)

                print('calculate performance ledger for portfolio(%s) of user(%s), trade date is %s' % (self.portfolio_name, self.u_name, _trade_date_str))

                last_net_value = NetValueLedgerModel.select().where(NetValueLedgerModel.trade_date == _day_before_trade_date_str).get()
                current_net_value = NetValueLedgerModel.select().where(NetValueLedgerModel.trade_date == _trade_date_str).get()
                last_performance = PerformanceLedgerModel.select().where(PerformanceLedgerModel.trade_date == _day_before_trade_date_str).get()
                performances = PerformanceLedgerModel.select().where(PerformanceLedgerModel.trade_date <= _day_before_trade_date_str)

                max_net_value = NetValueLedgerModel.select(fn.MAX(NetValueLedgerModel.net_value)).where(NetValueLedgerModel.trade_date <= _trade_date_str).scalar()
                max_retracement_range_history = PerformanceLedgerModel.select(fn.MIN(PerformanceLedgerModel.max_retracement_range)).where(PerformanceLedgerModel.trade_date <= _trade_date_str).scalar() # value is minus, so select the MIN
                max_days_of_continuous_loss_history = PerformanceLedgerModel.select(fn.MAX(PerformanceLedgerModel.days_of_continuous_loss)).where(PerformanceLedgerModel.trade_date <= _trade_date_str).scalar()
                days_of_win_history = PerformanceLedgerModel.select(fn.COUNT(PerformanceLedgerModel.trade_date)).where(PerformanceLedgerModel.trade_date <= _trade_date_str, PerformanceLedgerModel.change_percentage > 0).scalar()
                days_of_loss_history = PerformanceLedgerModel.select(fn.COUNT(PerformanceLedgerModel.trade_date)).where(PerformanceLedgerModel.trade_date <= _trade_date_str, PerformanceLedgerModel.change_percentage < 0).scalar()
                total_trade_count = TransactionLedgerModel.select(fn.COUNT(TransactionLedgerModel.trade_date)).where(TransactionLedgerModel.trade_date <= _trade_date_str, TransactionLedgerModel.trade_type == 'sell').scalar()

                change_percentage = round((current_net_value.net_value - last_net_value.net_value) / last_net_value.net_value, 3)
                retracement_range = round((current_net_value.net_value - max_net_value) / max_net_value, 3)
                max_retracement_range = retracement_range if retracement_range < max_retracement_range_history else max_retracement_range_history
                days_of_continuous_loss = last_performance.days_of_continuous_loss + 1 if change_percentage < 0 else 0
                max_days_of_continuous_loss = days_of_continuous_loss if days_of_continuous_loss > max_days_of_continuous_loss_history else max_days_of_continuous_loss_history
                days_of_win = days_of_win_history + 1 if change_percentage > 0 else days_of_win_history
                days_of_loss = days_of_loss_history + 1 if change_percentage < 0 else days_of_loss_history
                run_days = last_performance.run_days + 1
                cagr = round(CAGR(1.0, current_net_value.net_value, float(run_days/365)), 3)
                sharpe_ratio = SHARPE_RATIO(pd.DataFrame(list(performances.dicts()))['change_percentage']) # not contain current performance data because it has not yet saved in database

                PerformanceLedgerModel.insert(trade_date=_trade_date_str, \
                                            change_percentage=change_percentage, \
                                            retracement_range=retracement_range, \
                                            max_retracement_range=max_retracement_range, \
                                            days_of_continuous_loss=days_of_continuous_loss, \
                                            max_days_of_continuous_loss=max_days_of_continuous_loss, \
                                            days_of_win=days_of_win, \
                                            days_of_loss=days_of_loss, \
                                            run_days=run_days, \
                                            total_trade_count=total_trade_count, \
                                            cagr=cagr, \
                                            sharpe_ratio=sharpe_ratio, \
                                            hold_risk_count=0, \
                                            buy_risk_count=0).on_conflict_replace().execute()
            except Exception as e:
                print('Exception: %s' % e)

    def update_net_value(self, trade_date):
        self.__update_transaction_ledger(trade_date)
        self.__update_funding_ledger(trade_date)
        self.__update_holding_ledger(trade_date)
        self.__update_net_value_ledger(trade_date)
        self.__update_performance_ledger(trade_date)