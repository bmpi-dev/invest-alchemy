from peewee import *
from storage import db

class BaseModel(Model):
    class Meta:
        database = db

class DmaTradeSignal(BaseModel):
    trade_date = TextField()
    trade_code = TextField()
    trade_name = TextField(null=True)
    trade_timestamp = IntegerField(constraints=[SQL("DEFAULT strftime('%s','now')")], null=True)
    trade_type = IntegerField(null=True)

    class Meta:
        table_name = 'dma_trade_signal'
        indexes = (
            (('trade_date', 'trade_code'), True),
        )
        primary_key = CompositeKey('trade_code', 'trade_date')
