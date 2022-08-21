from constants import LOCAL_BASE_DIR, S3_PORTFOLIO_BASE_DIR
from os.path import exists
from storage import s3_client
import botocore
from constants import S3_BUCKET_NAME
from peewee import SqliteDatabase
import os

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
        self.portfolio_db = None

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
        if (self.portfolio_db is None):
            print('start connect database for portfolio(%s) ot user(%s)' % (self.portfolio_name, self.u_name))
            self.portfolio_db = SqliteDatabase(self.portfolio_db_local_path)
            self.portfolio_db.connect()

    def finish(self):
        if (exists(self.portfolio_db_local_path)):
            print('start disconnect database for portfolio(%s) ot user(%s)' % (self.portfolio_name, self.u_name))
            if (self.portfolio_db is None):
                self.portfolio_db.close()
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
        pass

    def __update_funding_ledger(self, trade_date):
        """Update funding ledger on the given trade date

        :param trade_date: trade date
        :return: None
        """
        pass

    def __update_holding_ledger(self, trade_date):
        """Update holding ledger on the given trade date

        :param trade_date: trade date
        :return: None
        """
        pass

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