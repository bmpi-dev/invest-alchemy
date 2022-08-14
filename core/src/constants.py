from datetime import datetime
import os

AWS_REGION = 'us-east-1'
S3_BUCKET_NAME = 'i365.tech'
S3_DOUBLE_MA_BASE_DIR = 'invest-alchemy/data/strategy/double-ma/'
S3_SQLITE_DB_BASE_DIR = 'invest-alchemy/data/db/'
LOCAL_SQLITE_DB_BASE_DIR = '/tmp/'
SQLITE_DB_FILE = 'base.db'
OUTPUT_FILE = datetime.today().strftime('%Y%m%d') + '.txt'
SNS_TOPIC = 'arn:aws:sns:us-east-1:745121664662:trade-signal-topic'
TODAY_STR = datetime.today().strftime('%Y%m%d')
TG_CHATS = os.environ['TG_CHAT_IDS'].split(' ')
TG_SEND_MESSAGE_API='https://api.telegram.org/bot' + os.environ['TG_BOT_API_TOKEN'] + '/sendMessage'
STRATEGY_DMA_SHORT_TERM = 11
STRATEGY_DMA_LONG_TERM = 22