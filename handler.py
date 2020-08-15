try:
  import unzip_requirements
except ImportError:
  pass
import json
import numpy as np
import tushare as ts
import os
from datetime import datetime, timedelta

def run(pro, code, name):
    start = (datetime.today() - timedelta(days=150)).strftime('%Y%m%d')
    end = datetime.today().strftime('%Y%m%d')
    data = pro.fund_daily(ts_code=code, start_date=start, end_date=end).sort_index(ascending=False)
    close_price = np.array(data['close'])
    print(close_price)

def invest(event, context):
    pro = ts.pro_api(os.environ['TUSHARE_API_TOKEN'])

    with open("fund.txt", "r") as f:
        for line in f:
            code_name = line.split(",")
            run(pro, code_name[0], code_name[1].rstrip())
    
    response = {
        "statusCode": 200,
    }

    return response
