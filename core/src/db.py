from peewee import *
from storage import db

class BaseModel(Model):
    class Meta:
        database = db

class DmaTradeSignalModel(BaseModel):
    trade_code = CharField()
    trade_date = CharField()
    trade_name = CharField(null=True)
    trade_type = CharField()
    strategy_type = CharField(null=True)
    trade_timestamp = DateTimeField(constraints=[SQL("DEFAULT (now() AT TIME ZONE 'utc'::text)")], null=True)

    class Meta:
        table_name = 'dma_trade_signal'
        indexes = (
            (('trade_date', 'trade_code'), True),
        )
        primary_key = CompositeKey('trade_code', 'trade_date')

class IndexDailyModel(BaseModel):
    trade_code = CharField()
    trade_date = CharField()
    trade_name = CharField(null=True)
    open_price = DoubleField()
    close_price = DoubleField()
    high_price = DoubleField()
    low_price = DoubleField()
    change = DoubleField()
    pct_chg = DoubleField()
    trade_timestamp = DateTimeField(constraints=[SQL("DEFAULT (now() AT TIME ZONE 'utc'::text)")], null=True)

    class Meta:
        table_name = 'index_daily'
        indexes = (
            (('trade_date', 'trade_code'), True),
        )
        primary_key = CompositeKey('trade_code', 'trade_date')

class Portfolio(BaseModel):
    trader_id = IntegerField()
    portfolio_name = CharField()
    comment = TextField(null=True)
    portfolio_status = CharField(null=True)
    update_timestamp = DateTimeField(constraints=[SQL("DEFAULT (now() AT TIME ZONE 'utc'::text)")], null=True)
    create_timestamp = DateTimeField(constraints=[SQL("DEFAULT (now() AT TIME ZONE 'utc'::text)")], null=True)

    class Meta:
        table_name = 'portfolio'

class Trader(BaseModel):
    username = CharField(null=True, unique=True)
    email = CharField(null=True)
    nickname = CharField(null=True)
    trader_status = CharField(null=True)
    trader_type = CharField(null=True)
    update_timestamp = DateTimeField(constraints=[SQL("DEFAULT (now() AT TIME ZONE 'utc'::text)")], null=True)
    create_timestamp = DateTimeField(constraints=[SQL("DEFAULT (now() AT TIME ZONE 'utc'::text)")], null=True)

    class Meta:
        table_name = 'trader'