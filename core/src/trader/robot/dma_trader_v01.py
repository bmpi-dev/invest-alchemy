from trader.trader import ITrader

def DMATraderV01(ITrader):
    """Robot trader(V01) who follow the Double MA strategy(MA parameter: 11/22)
       Note: One robot trader only can have one trade protfolio
    """

    def __init__(self):
        self.u_name = 'robot_dma_v01'

    def get_protfolios() -> List[str]:
        pass

    def update_protfolios(self, trade_date):
        pass

    def __generate_transaction_with_strategy_signal(self, trade_date):
        """Generate transaction record with strategy by given trade date

        :param trade_date: trade date
        :return: None
        """
        pass

    def __generate_funding_with_funding_strategy(self, trade_date):
        """Generate funding record with funding strategy by given trade date

        :param trade_date: trade date
        :return: None
        """
        pass