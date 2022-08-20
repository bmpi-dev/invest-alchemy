from abc import ABCMeta, abstractmethod, abstractproperty
from typing import Sequence
from strategy.trade_signal import TradeSignal

class IStrategy(metaclass=ABCMeta):
    @abstractproperty
    def trade_signals(self) -> Sequence[TradeSignal]:
        """Get the trade signals

        :return: List of TradeSignal
        """
        pass

    @abstractmethod
    def process(self, file_path):
        """Get the trade signals

        :param file_path: file path of the trade targets
        :return: None
        """
        pass

    @abstractmethod
    def save_signals_to_db(self):
        """Save the trade signals to db

        :return: None
        """
        pass