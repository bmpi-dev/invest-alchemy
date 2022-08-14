from abc import ABCMeta, abstractmethod, abstractproperty
from typing import Sequence
from strategy.trade_signal import TradeSignal
from db import DmaTradeSignalModel
from constants import TODAY_STR


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

    def save_signals_to_db(self):
        for signal in self.trade_signals:
            state = signal.state
            code = signal.code
            name = signal.name
            DmaTradeSignalModel.insert(trade_date=TODAY_STR, trade_code=code, trade_name=name, trade_type=state.value).on_conflict_replace().execute()