from peewee import *
from datetime import datetime
import time

portfolio_db = SqliteDatabase(None)  # Defer initialization


def re_bind_db(db_path):
    """Re-bind database when portfolio initialization
    """
    print('re-bind database, path is (%s)' % db_path)
    portfolio_db.init(db_path, pragmas={'journal_mode': 'wal'})
    portfolio_db.bind([FundingLedgerModel, TransactionLedgerModel, HoldingLedgerModel, NetValueLedgerModel, PerformanceLedgerModel, IndexCompareLedgerModel])
    portfolio_db.connect()
    portfolio_db.create_tables([FundingLedgerModel, TransactionLedgerModel, HoldingLedgerModel, NetValueLedgerModel, PerformanceLedgerModel, IndexCompareLedgerModel])

def disconnect_db():
    portfolio_db.close()

class PortfolioBaseModel(Model):
    trade_date = TextField(index=True)
    create = IntegerField(default=time.mktime(datetime.now().timetuple()))

class FundingLedgerModel(PortfolioBaseModel):
    fund_amount = FloatField()
    current_available_amount = FloatField()
    fund_type = TextField()

    class Meta:
        table_name = 'portfolio_funding_ledger'

class TransactionLedgerModel(PortfolioBaseModel):
    trade_code = TextField()
    trade_name = TextField()
    trade_type = TextField()
    trade_amount = FloatField()
    current_available_amount = FloatField()
    trade_price = FloatField()
    trade_money = FloatField()
    handling_fees = FloatField()
    funding_percentage = FloatField() # this transaction funds as a percentage of total funds

    class Meta:
        table_name = 'portfolio_transaction_ledger'

class HoldingLedgerModel(PortfolioBaseModel):
    trade_code = TextField()
    trade_name = TextField()
    hold_amount = FloatField()
    close_price = FloatField()
    market_value = FloatField()
    position_percentage = FloatField() # this position as a percentage of the total position

    class Meta:
        table_name = 'portfolio_holding_ledger'
        primary_key = CompositeKey('trade_date', 'trade_code')

class NetValueLedgerModel(PortfolioBaseModel):
    net_value = FloatField()
    total_shares = FloatField()
    total_assets = FloatField()
    hold_assets = FloatField()
    fund_balance = FloatField()

    class Meta:
        table_name = 'portfolio_net_value_ledger'
        primary_key = CompositeKey('trade_date')

class PerformanceLedgerModel(PortfolioBaseModel):
    change_percentage = FloatField() # daily change percentage
    retracement_range = FloatField() # drawback percentage
    max_retracement_range = FloatField() # max drawback percentage in history
    days_of_continuous_loss = IntegerField()
    max_days_of_continuous_loss = IntegerField()
    days_of_win = IntegerField()
    days_of_loss = IntegerField()
    run_days = IntegerField()
    total_trade_count = IntegerField()
    cagr = FloatField()
    sharpe_ratio = FloatField()
    hold_risk_count = IntegerField() # reserved
    buy_risk_count = IntegerField() # reserved

    class Meta:
        table_name = 'portfolio_performance_ledger'
        primary_key = CompositeKey('trade_date')

class IndexCompareLedgerModel(PortfolioBaseModel):
    portfolio_nv = FloatField() # portfolio net value
    zz500 = FloatField() # 000905.SH index point
    zz500_nv = FloatField() # 000905.SH net value
    hs300 = FloatField() # 000300.SH index point
    hs300_nv = FloatField() # 000300.SH net value
    cyb = FloatField() # 399006.SZ index point
    cyb_nv = FloatField() # 399006.SZ net value
    hsi = FloatField() # HSI index point
    hsi_nv = FloatField() # HSI net value
    spx = FloatField() # SPX index point
    spx_nv = FloatField() # SPX net value
    ixic = FloatField() # IXIC index point
    ixic_nv = FloatField() # IXIC net value
    gdaxi = FloatField() # GDAXI index point
    gdaxi_nv = FloatField() # GDAXI net value
    n225 = FloatField() # N225 index point
    n225_nv = FloatField() # N225 net value
    ks11 = FloatField() # KS11 index point
    ks11_nv = FloatField() # KS11 net value
    as51 = FloatField() # AS51 index point
    as51_nv = FloatField() # AS51 net value
    sensex = FloatField() # SENSEX index point
    sensex_nv = FloatField() # SENSEX net value
    base15_nv = FloatField() # 15% base year net value

    class Meta:
        table_name = 'portfolio_index_compare_ledger'
        primary_key = CompositeKey('trade_date')