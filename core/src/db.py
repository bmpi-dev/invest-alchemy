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
