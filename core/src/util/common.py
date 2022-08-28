from datetime import datetime
from constants import TRADE_DATE_FORMAT_STR
from client.ts_client import TSClient

trade_client = TSClient()

def get_trade_close_price(trade_date, trade_code):
    data = trade_client.get_qfq_close_price(trade_code, trade_date, trade_date)
    return round(data['close'][0].item(), 3)

def get_qfq_close_price(code, start, end):
    return trade_client.get_qfq_close_price(code, start, end)

def get_trade_date_range(start, end):
    return trade_client.get_a_share_trade_date(start, end)

def trade_date_big(left, right):
     return datetime.strptime(left, TRADE_DATE_FORMAT_STR) > datetime.strptime(right, TRADE_DATE_FORMAT_STR)
