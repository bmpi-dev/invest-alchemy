from client.ts_client import TSClient, ITradeDataClient
from db import IndexDailyModel
from constants import TRADE_DATE_FORMAT_STR, TODAY_STR
from datetime import datetime, timedelta
from peewee import DoesNotExist
import traceback

MAX_DAYS = 4000 # 10 years data

class IndexDaily:

    def __init__(self, client: ITradeDataClient):
        self.__client = client

    def __is_global_index(self, code):
        return False if code.endswith('.SH') or code.endswith('.SZ') else True

    def process(self):
        with open('data/index.txt', "r") as f:
            for line in f:
                code_name = line.split(",")
                code = code_name[0]
                name = code_name[1]
                try:
                    last_record_db = IndexDailyModel.select().where(IndexDailyModel.trade_code == code).order_by(IndexDailyModel.trade_date.desc()).get()
                    start_date = last_record_db.trade_date
                except DoesNotExist:
                    start_date = (datetime.today() - timedelta(MAX_DAYS)).strftime(TRADE_DATE_FORMAT_STR)
                try:
                    if (self.__is_global_index(code)):
                        data = self.__client.get_ts().index_global(ts_code=code, start_date=start_date, end_date=TODAY_STR).sort_index(ascending=False)
                    else:
                        data = self.__client.get_ts().index_daily(ts_code=code, start_date=start_date, end_date=TODAY_STR).sort_index(ascending=False)
                    for row in data.itertuples():
                        print('save index(%s) on trade date(%s)...' % (code, row.trade_date))
                        IndexDailyModel.insert(trade_date=row.trade_date, \
                                            trade_code=code, \
                                            trade_name=name, \
                                            open_price=round(row.open, 4), \
                                            close_price=round(row.close, 4), \
                                            high_price=round(row.high, 4), \
                                            low_price=round(row.low, 4), \
                                            change=round(row.change, 4), \
                                            pct_chg=round(row.pct_chg, 4) \
                                            ).on_conflict(conflict_target=[IndexDailyModel.trade_date, IndexDailyModel.trade_code], \
                                            preserve=[IndexDailyModel.open_price, IndexDailyModel.close_price, IndexDailyModel.high_price, \
                                            IndexDailyModel.low_price, IndexDailyModel.change, IndexDailyModel.pct_chg, IndexDailyModel.trade_timestamp]).execute()
                except Exception as e:
                    print(e)
                    traceback.print_exc()