import csv
from os.path import exists
from operator import itemgetter
from client.ts_client import TSClient
from portfolio.trade_portfolio import Portfolio
from util.common import trade_date_big

FUNDING_LEDGER_CSV_HEADER = ['trade_date', 'fund_amount', 'fund_type', 'current_available_amount']
TRANSACTION_LEDGER_CSV_HEADER = ['trade_date', 'trade_code', 'trade_name', 'trade_type', 'trade_amount', 'trade_price', 'current_available_amount']
trade_client = TSClient()

def __get_trade_target_last_transaction_record(transaction_ledger_path, trade_code):
    with open(transaction_ledger_path, 'r', newline='') as csvfile:
        rows = csv.DictReader(csvfile)
        data = list(rows)
        for r in reversed(data):
            if (r['trade_code'] == trade_code):
                return r

def get_trade_qfq_price(trade_date, trade_code):
    data = trade_client.get_qfq_close_price(trade_code, trade_date, trade_date)
    return round(data['qfq'][0].item(), 2)

def get_current_available_funding(funding_ledger_path):
    with open(funding_ledger_path, 'r', newline='') as csvfile:
        rows = csv.DictReader(csvfile)
        data = list(rows)
        if (len(data) < 1):
            raise Exception('can not find available funding record in funding_ledger_path(%s)' % funding_ledger_path)
        return data[-1]['trade_date'], round(float(data[-1]['current_available_amount']), 2)

def get_trade_amount_last_transaction_record(transaction_ledger_path, trade_code):
    r = __get_trade_target_last_transaction_record(transaction_ledger_path, trade_code)
    if (r is not None):
        return round(float(r['trade_amount']), 2)

def get_last_trade_date(p: Portfolio):
    with open(p.transaction_local_ledger, 'r', newline='') as csvfile:
        rows = csv.DictReader(csvfile)
        data = list(rows)
        if (len(data) > 0):
            return data[-1]['trade_date']
    return p.create_date

def get_trade_date_range(start, end):
    return trade_client.get_a_share_trade_date(start, end)

def update_funding_ledger(new_row, funding_ledger_path, is_init=False):
    trade_date, fund_amount, fund_type = itemgetter('trade_date', 'fund_amount', 'fund_type')(new_row)
    if (not is_init):
        if (fund_type not in ['in', 'out', 'buy', 'sell']):
            raise Exception('cannot update funding ledger for portfolio, because fund_type is not valid, funding_ledger_path is (%s), add row data is (%s)' % (funding_ledger_path, new_row))
        is_fund_amount_valid = True
        if (fund_type == 'in' or fund_type == 'sell'):
            if (fund_amount <= 0):
                is_fund_amount_valid = False
        if (fund_type == 'out' or fund_type == 'buy'):
            if (fund_amount >= 0):
                is_fund_amount_valid = False
        if not is_fund_amount_valid:
            raise Exception('cannot update funding ledger for portfolio, because fund_amount is not valid, funding_ledger_path is (%s), add row data is (%s)' % (funding_ledger_path, new_row))
        last_trade_date, last_current_available_amount = get_current_available_funding(funding_ledger_path)
        if (trade_date_big(last_trade_date, trade_date)):
            raise Exception('cannot update funding ledger for portfolio, because trade_date is not valid, funding_ledger_path is (%s), add row data is (%s)' % (funding_ledger_path, new_row))
        update_current_available_amount = last_current_available_amount + fund_amount
        if (update_current_available_amount < 0):
            raise Exception('cannot update funding ledger for portfolio, because fund_amount is not valid, funding_ledger_path is (%s), add row data is (%s)' % (funding_ledger_path, new_row))
    else:
        if (fund_type != 'in'):
            raise Exception('cannot update funding ledger for portfolio, because init fund_type must is in, funding_ledger_path is (%s), add row data is (%s)' % (funding_ledger_path, new_row))
        if (fund_amount <= 0):
            raise Exception('cannot update funding ledger for portfolio, because init fund_amount must greater than 0, funding_ledger_path is (%s), add row data is (%s)' % (funding_ledger_path, new_row))
        update_current_available_amount = fund_amount
    with open(funding_ledger_path, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=FUNDING_LEDGER_CSV_HEADER)
        writer.writerow({'trade_date': trade_date, 'fund_amount': str(fund_amount), 'fund_type': fund_type, 'current_available_amount': str(update_current_available_amount)})

def update_transaction_ledger(new_row, transaction_ledger_path):
    trade_date, trade_code, trade_name, trade_type, trade_amount, trade_price = itemgetter('trade_date', 'trade_code', 'trade_name', 'trade_type', 'trade_amount', 'trade_price')(new_row)
    if (trade_type not in ['buy', 'sell']):
        raise Exception('cannot update transaction ledger for portfolio, because trade_type is not valid, transaction_ledger_path is (%s), add row data is (%s)' % (transaction_ledger_path, new_row))
    is_trade_amount_valid = True
    if (trade_type == 'buy'):
        if (trade_amount <= 0):
            is_trade_amount_valid = False
    if (trade_type == 'sell'):
        if (trade_amount >= 0):
            is_trade_amount_valid = False
    if not is_trade_amount_valid:
        raise Exception('cannot update transaction ledger for portfolio, because trade_amount is not valid, transaction_ledger_path is (%s), add row data is (%s)' % (transaction_ledger_path, new_row))

    last_transaction = __get_trade_target_last_transaction_record(transaction_ledger_path, trade_code)
    if last_transaction is not None:
        if (trade_date_big(last_transaction['trade_date'], trade_date)):
            raise Exception('cannot update transaction ledger for portfolio, because trade_date is not valid, transaction_ledger_path is (%s), add row data is (%s)' % (transaction_ledger_path, new_row))
        update_current_available_amount = round(float(last_transaction['current_available_amount']), 2) + trade_amount
    else:
        if (trade_type == 'sell'):
            raise Exception('cannot update transaction ledger for portfolio, because can not find last transaction record, transaction_ledger_path is (%s), add row data is (%s)' % (transaction_ledger_path, new_row))
        update_current_available_amount = trade_amount
    if (update_current_available_amount < 0):
        raise Exception('cannot update transaction ledger for portfolio, because trade_amount is not valid, transaction_ledger_path is (%s), add row data is (%s)' % (transaction_ledger_path, new_row))
    with open(transaction_ledger_path, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=TRANSACTION_LEDGER_CSV_HEADER)
        writer.writerow({'trade_date': trade_date, 'trade_code': trade_code, 'trade_name': trade_name, 'trade_type': trade_type, 'trade_amount': str(trade_amount), 'trade_price': str(trade_price), 'current_available_amount': str(update_current_available_amount)})