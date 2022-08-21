from datetime import datetime
from constants import TRADE_DATE_FORMAT_STR

def trade_date_big(left, right):
     return datetime.strptime(left, TRADE_DATE_FORMAT_STR) > datetime.strptime(right, TRADE_DATE_FORMAT_STR)
