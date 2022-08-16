from abc import ABCMeta, abstractmethod

class ITradeDataClient(metaclass=ABCMeta):
    @abstractmethod
    def get_qfq_close_price(self, code, start, end):
        """Get qfq close price

        :param code: trade target code
        :param code: start date
        :param code: end date
        :return: DataFrame
        """
        pass