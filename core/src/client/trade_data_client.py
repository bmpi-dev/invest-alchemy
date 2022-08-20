from abc import ABCMeta, abstractmethod

class ITradeDataClient(metaclass=ABCMeta):
    @abstractmethod
    def get_qfq_close_price(self, code, start, end):
        """Get qfq close price

        :param code: trade target code
        :param start: start date
        :param end: end date
        :return: DataFrame
        """
        pass

    @abstractmethod
    def get_a_share_trade_date(self, start, end) -> [str]:
        """Get A share trade date

        :param start: start date
        :param end: end date
        :return: List of trade date str
        """
        pass