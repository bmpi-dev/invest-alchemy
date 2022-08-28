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
from util.common import get_trade_close_price, get_qfq_close_price

class Portfolio:
    """Trade Portfolio class"""

    def __init__(self, u_name, portfolio_name, create_date):
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

    def __init_work_dir(self):
        if (exists(self.portfolio_db_local_path)):
            print('delete local files for portfolio(%s) of user(%s)' % (self.portfolio_name, self.u_name))
            try:
                os.remove(self.portfolio_db_local_path)
                os.remove(self.transaction_local_ledger)
                os.remove(self.funding_local_ledger)
            except Exception(e):
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
            s3_client.upload_file(self.portfolio_db_local_path, S3_BUCKET_NAME, self.portfolio_db_remote_path, ExtraArgs={'ACL': 'public-read'})
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
            last_trade_date_db = self.create_date
        with open(self.transaction_local_ledger, 'r', newline='') as csvfile:
            rows = csv.DictReader(csvfile)
            for row in rows:
                trade_date_csv = row['trade_date']
                if (trade_date_big(trade_date_csv, last_trade_date_db)):
                    print('update transaction ledger of portfolio(%s) for user(%s), trade date: %s...' % (self.portfolio_name, self.u_name, trade_date_csv))
                    trade_amount=round(float(row['trade_amount']), 3)
                    trade_price=round(float(row['trade_price']), 3)
                    trade_money=round(trade_amount * trade_price, 3)
                    current_available_amount=round(float(row['current_available_amount']), 3)
                    save_db = TransactionLedgerModel(trade_date=trade_date_csv, \
                                                    trade_code=row['trade_code'], \
                                                    trade_name=row['trade_name'], \
                                                    trade_type=row['trade_type'], \
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
            last_trade_date_db = self.create_date
        with open(self.funding_local_ledger, 'r', newline='') as csvfile:
            rows = csv.DictReader(csvfile)
            for row in rows:
                trade_date_csv = row['trade_date']
                if (trade_date_big(trade_date_csv, last_trade_date_db)):
                    print('update funding ledger of portfolio(%s) for user(%s), trade date: %s...' % (self.portfolio_name, self.u_name, trade_date_csv))
                    fund_amount=round(float(row['fund_amount']), 3)
                    current_available_amount=round(float(row['current_available_amount']), 3)
                    save_db = FundingLedgerModel(trade_date=trade_date_csv, \
                                                   fund_amount=fund_amount, \
                                                   current_available_amount=current_available_amount, \
                                                   fund_type=row['fund_type'])
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
                    if (transaction.current_available_amount > 0):
                        close_price = get_trade_close_price(first_transaction_date, transaction.trade_code)
                        market_value = transaction.current_available_amount * close_price
                        HoldingLedgerModel.insert(trade_date=first_transaction_date, \
                                                  trade_code=transaction.trade_code, \
                                                  trade_name=transaction.trade_name, \
                                                  hold_amount=transaction.current_available_amount, \
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
                    if (adj_factor != 1.0):
                        print('process split-adjusted share prices case: holding code(%s) with trade date(%s), found adj_factor(%d) for portfolio(%s) of user(%s)' % (hold.trade_code, _trade_date_str, adj_factor, self.portfolio_name, self.u_name))
                        hold.hold_amount = round(hold.hold_amount * adj_factor, 3)
                        hold.market_value = round(hold.close_price * hold.hold_amount, 3)
                except Exception as e:
                    print(e)
                if (hold.hold_amount <= 0):
                    print('remove hold: %s' % hold.trade_code)
                else:
                    HoldingLedgerModel.insert(trade_date=hold.trade_date, \
                                              trade_code=hold.trade_code, \
                                              trade_name=hold.trade_name, \
                                              hold_amount=hold.hold_amount, \
                                              close_price=hold.close_price, \
                                              market_value=hold.market_value, \
                                              position_percentage=hold.position_percentage).on_conflict_replace().execute()

    def __update_performance_ledger(self, trade_date):
        """Update portfolio performance ledger on the given trade date

        :param trade_date: trade date
        :return: None
        """
        pass

    def update_net_value_ledger(self, trade_date):
        """Update portfolio net value ledger on the given trade date

        :param trade_date: trade date
        :return: None
        """
        self.__update_transaction_ledger(trade_date)
        self.__update_funding_ledger(trade_date)
        self.__update_holding_ledger(trade_date)
        # TODO: calculate net value ledger
        print('calculate net value ledger for portfolio(%s) of user(%s), trade date is %s' % (self.portfolio_name, self.u_name, trade_date))
        self.__update_performance_ledger(trade_date)