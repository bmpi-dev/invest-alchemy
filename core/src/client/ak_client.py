from client.trade_data_client import ITradeDataClient

class AKClient(ITradeDataClient):
    
    def get_qfq_close_price(self, code, start, end):
        pass

    def get_a_share_trade_date(self, start, end) -> [str]:
        pass