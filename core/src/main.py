import talib as ta
import numpy as np
import tushare as ts
import matplotlib.pyplot as plt
import pandas as pd
import os
import sys
from datetime import datetime, timedelta
import boto3

AWS_REGION = 'us-east-1'
S3_BUCKET_NAME = 'i365.tech'
S3_DOUBLE_MA_BASE_DIR = 'invest-alchemy/data/strategy/double-ma/'
OUTPUT_FILE = datetime.today().strftime('%Y%m%d') + '.txt'
SNS_TOPIC = 'arn:aws:sns:us-east-1:745121664662:trade-signal-topic'

TODAY_STR = datetime.today().strftime('%Y%m%d')

pro = ts.pro_api(os.environ['TUSHARE_API_TOKEN'])

start = (datetime.today() - timedelta(days=150)).strftime('%Y%m%d')
end = TODAY_STR

short_term = 11
long_term = 22

buy_codes = []
sell_codes = []
hold_codes = []
empty_codes = []

class Logger(object):
    def __init__(self):
        self.terminal = sys.stdout
        self.log = open('/tmp/' + OUTPUT_FILE, "w")
        self.is_open = True

    def open(self):
        self.terminal = sys.stdout
        self.log = open('/tmp/' + OUTPUT_FILE, "w")
        self.is_open = True

    def close(self):
        self.log.close()
        self.is_open = False

    def write(self, message):
        self.terminal.write(message)
        if self.is_open:
            self.log.write(message)

    def flush(self):
        #this flush method is needed for python 3 compatibility.
        #this handles the flush command by doing nothing.
        #you might want to specify some extra behavior here.
        pass

sys.stdout = Logger()

def run(code, name):
    adj = pro.fund_adj(ts_code=code, start_date=start, end_date=end).sort_index(ascending=False)
    data = pro.fund_daily(ts_code=code, start_date=start, end_date=end).sort_index(ascending=False)
    data = data.merge(adj, on='trade_date')
    qfq_close_price = data['close'].multiply(data['adj_factor']) / data['adj_factor'].iloc[-1]
    close_price = np.array(qfq_close_price)
    time = np.array(data['trade_date'])
    short_ma = np.round(ta.MA(close_price, short_term), 3)
    long_ma = np.round(ta.MA(close_price, long_term), 3)
    if (short_ma[-1] > long_ma[-1] and short_ma[-2] <= long_ma[-2]):
        s = name + "(" + str(code) + ")" + "可买, 收盘价" + str(close_price[-1]) + ", 11日均线" + str(short_ma[-1]) + ", 22日均线" + str(long_ma[-1])
        buy_codes.append(s)
    elif (short_ma[-1] < long_ma[-1] and short_ma[-2] >= long_ma[-2]):
        s = name + "(" + str(code) + ")" + "可卖, 收盘价" + str(close_price[-1]) + ", 11日均线" + str(short_ma[-1]) + ", 22日均线" + str(long_ma[-1])
        sell_codes.append(s)
    else:
        if short_ma[-1] > long_ma[-1]:
            for i in range(1, len(long_ma)):
                if short_ma[-1 - i] <= long_ma[-1 - i]:
                    s = datetime.strptime(time[-1 - i], '%Y%m%d')
                    e = datetime.strptime(time[-1], '%Y%m%d')
                    interval_days = (e - s).days
                    s = name + "(" + str(code) + ")" + "于" + str(time[-1 - i]) + "日买入, " + "持有" + str(interval_days) + "天, 盈利" + str(round((close_price[-1] - close_price[-1 -i]) / close_price[-1 -i] * 100, 2)) + "%"
                    hold_codes.append(s)
                    break
        if short_ma[-1] < long_ma[-1]:
            for i in range(1, len(long_ma)):
                if short_ma[-1 - i] >= long_ma[-1 - i]:
                    s = datetime.strptime(time[-1 - i], '%Y%m%d')
                    e = datetime.strptime(time[-1], '%Y%m%d')
                    interval_days = (e - s).days
                    s = name + "(" + str(code) + ")" + "于" + str(time[-1 - i]) + "日卖出, " + "空仓" + str(interval_days) + "天, 空仓期涨幅" + str(round((close_price[-1] - close_price[-1 -i]) / close_price[-1 -i] * 100, 2)) + "%"
                    empty_codes.append(s)
                    break

def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client('s3', region_name=AWS_REGION)
    try:
        response = s3_client.upload_file(file_name, bucket, object_name, ExtraArgs={'ACL': 'public-read', 'ContentType': 'text/plain; charset=utf-8'})
    except ClientError as e:
        logging.error(e)
        return False
    return True

def send_sns(file_name):
    """Send message by sns
    Amazon SNS is designed to distribute notifications, If you wish to send formatted emails, consider using Amazon Simple Email Service (SES), which improves email deliverability.
    """
    subject = 'Double MA Strategy Trade Signal: ' + TODAY_STR + ' - A Share'
    with open(file_name, 'r') as file:
        message = file.read()
        sns_client = boto3.client('sns', region_name=AWS_REGION)
        sns_client.publish(
            TopicArn=SNS_TOPIC,
            Message=message,
            Subject=subject,
        )

def make_trade_signal():
    with open("fund.txt", "r") as f:
        for line in f:
            code_name = line.split(",")
            run(code_name[0], code_name[1].rstrip())
    
    print('可买标的:')
    for code in buy_codes:
        print(code)
    print('#########################################')
    print('可卖标的:')
    for code in sell_codes:
        print(code)
    print('#########################################')
    print('持仓标的:')
    for code in hold_codes:
        print(code)
    print('#########################################')
    print('空仓标的:')
    for code in empty_codes:
        print(code)

if __name__ == "__main__":
    make_trade_signal()
    sys.stdout.close()
    print('\nstart upload output file to s3...\n')
    upload_file('/tmp/' + OUTPUT_FILE, S3_BUCKET_NAME, S3_DOUBLE_MA_BASE_DIR + OUTPUT_FILE)
    print('end upload output file to s3\n')
    print('start send sns...\n')
    send_sns('/tmp/' + OUTPUT_FILE)
    print('end send sns...\n')