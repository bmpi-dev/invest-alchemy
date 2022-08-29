from peewee import *
import time
from datetime import datetime
import pandas as pd

portfolio_db = SqliteDatabase('/tmp/portfolio.db') 

class PortfolioBaseModel(Model):
    trade_date = TextField(index=True)
    create = IntegerField(default=time.mktime(datetime.now().timetuple()))

    class Meta:
        database = portfolio_db

class FundingLedgerModel(PortfolioBaseModel):
    fund_amount = FloatField()
    current_available_amount = FloatField()
    fund_type = TextField()

    class Meta:
        table_name = 'portfolio_funding_ledger'

portfolio_db.connect()
portfolio_db.create_tables([FundingLedgerModel])

# fund1 = FundingLedgerModel(trade_date='20200801', fund_amount=1230.0, current_available_amount=2221.0, fund_type='buy')
# fund2 = FundingLedgerModel(trade_date='20200802', fund_amount=2220.0, current_available_amount=2002.0, fund_type='buy')
# fund3 = FundingLedgerModel(trade_date='20200803', fund_amount=3000.0, current_available_amount=2003.0, fund_type='buy')
# fund1.save()
# fund2.save()
# fund3.save()

# fund = FundingLedgerModel.select().order_by(FundingLedgerModel.trade_date.desc()).get()
data = FundingLedgerModel.select().where(FundingLedgerModel.trade_date <= '20200803')
print(pd.DataFrame(list(data.dicts()))['fund_amount'] - 1000)
print(float(pd.DataFrame(list(data.dicts()))['fund_amount'].mean()))
print(float(pd.DataFrame(list(data.dicts()))['fund_amount'].std()))
