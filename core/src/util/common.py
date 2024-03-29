from datetime import datetime, timedelta
from constants import TRADE_DATE_FORMAT_STR, RISK_FREE_INVEST_DEPOSIT_RATE
from client.ts_client import TSClient
from pandas import DataFrame
import math

trade_client = TSClient()

def get_trade_close_price(trade_date, trade_code):
    data = trade_client.get_qfq_close_price(trade_code, trade_date, trade_date)
    return round(data['close'][0].item(), 3)

def get_trade_qfq_price(trade_date, trade_code):
    data = trade_client.get_qfq_close_price(trade_code, trade_date, trade_date)
    return round(data['qfq'][0].item(), 3)

def get_qfq_close_price(code, start, end):
    return trade_client.get_qfq_close_price(code, start, end)

def get_trade_date_range(start, end):
    return trade_client.get_a_share_trade_date(start, end)

def trade_date_big(left, right):
     return datetime.strptime(left, TRADE_DATE_FORMAT_STR) > datetime.strptime(right, TRADE_DATE_FORMAT_STR)

def CAGR(first, last, periods):
    return (last/first) ** (1/periods) - 1

def SHARPE_RATIO(input: DataFrame) -> float:
    if (len(input) <= 0):
        return 0
    ave = (input - RISK_FREE_INVEST_DEPOSIT_RATE).mean()
    std = (input - RISK_FREE_INVEST_DEPOSIT_RATE).std()
    if float(std) == 0 or math.isnan(float(std)):
        return 0
    return round(float(ave / std), 3)

def is_trader_robot(name):
    return name.startswith('robot_')

def get_the_day_before_n(trade_day_str, n):
    the_day_before = datetime.strptime(trade_day_str, TRADE_DATE_FORMAT_STR) - timedelta(n)
    return the_day_before.strftime(TRADE_DATE_FORMAT_STR)

def get_the_day_after_n(trade_day_str, n):
    the_day_after = datetime.strptime(trade_day_str, TRADE_DATE_FORMAT_STR) + timedelta(n)
    return the_day_after.strftime(TRADE_DATE_FORMAT_STR)