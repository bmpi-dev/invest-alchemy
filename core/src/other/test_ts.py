# execute this code when needs
import sys, os

sys.path.append(os.getcwd())

from client.ts_client import TSClient

# test target adj factor

ts = TSClient()

# data = ts.get_qfq_close_price('601288.SH', '20190120', '20190123')
data = ts.get_qfq_close_price('159941', '20190120', '20190123')

print(data)
print(round(float(data['close'].iloc[-1]), 3))
print(round(float(data['close'].iloc[-2]), 3))
print(float(data['adj_factor'].iloc[-1] / data['adj_factor'].iloc[-2]) == 4)
