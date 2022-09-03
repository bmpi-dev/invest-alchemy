from client.trade_data_client import ITradeDataClient
import os
import tushare as ts

class TSClient(ITradeDataClient):

    def __init__(self):
        self.__pro = ts.pro_api(os.environ['TUSHARE_API_TOKEN'])

    def get_ts(self):
        return self.__pro

    def __is_stock(self, code):
        return True if (code.startswith('300') or code.startswith('60') or code.startswith('000') or code.startswith('688')) else False

    def __format_code(self, code):
        if (code.endswith('.SZ') or code.endswith('.SH')):
            return code
        if (code.startswith('300') or code.startswith('000') or code.startswith('15') or code.startswith('16') or code.startswith('18')):
            return code + '.SZ'
        if (code.startswith('60') or code.startswith('688') or code.startswith('50') or code.startswith('51') or code.startswith('52')):
            return code + '.SH'
    
    def get_qfq_close_price(self, code, start, end):
        code = self.__format_code(code)
        if (self.__is_stock(code)):
            adj = self.__pro.daily(ts_code=code, start_date=start, end_date=end).sort_index(ascending=False)
            data = self.__pro.adj_factor(ts_code=code, start_date=start, end_date=end).sort_index(ascending=False)
        else:
            adj = self.__pro.fund_adj(ts_code=code, start_date=start, end_date=end).sort_index(ascending=False)
            data = self.__pro.fund_daily(ts_code=code, start_date=start, end_date=end).sort_index(ascending=False)
        if (len(data) <= 0):
            raise Exception('no trade price data for code(%s), start(%s), end(%s)' % (code, start, end))
        data = data.merge(adj, on='trade_date')
        data['qfq'] = data['close'].multiply(data['adj_factor']) / data['adj_factor'].iloc[-1]
        return data

    def get_a_share_trade_date(self, start, end) -> [str]:
        data = self.__pro.trade_cal(exchange='SSE', start_date=start, end_date=end)
        return list(data[data['is_open'] == 1]['cal_date'])