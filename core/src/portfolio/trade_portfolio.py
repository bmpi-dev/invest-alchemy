from constants import LOCAL_BASE_DIR

class Portfolio:
    """Trade Portfolio class"""

    def __init__(self, u_name, portfolio_name):
        self.u_name = u_name
        self.portfolio_name = portfolio_name
        self.portfolio_base_path = LOCAL_BASE_DIR + 'portfolio/' + self.u_name + '/' + self.portfolio_name + '/'
        self.portfolio_db_path = self.portfolio_base_path + self.portfolio_name + '.db'
        self.transaction_ledger = self.portfolio_base_pat + 'transaction_ledger.csv'
        self.funding_ledger = self.portfolio_base_pat + 'funding_ledger.csv'

    def sync_files(self):
        # TODO: implement
        pass

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