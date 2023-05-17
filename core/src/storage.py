import boto3
import botocore
from constants import AWS_REGION, LOCAL_BASE_DIR, S3_BUCKET_NAME, S3_PREMIUM_USER_LIST, PG_DB_NAME, PG_DB_USER, PG_DB_PWD, PG_DB_URL, PG_PORT
from os.path import exists
from peewee import PostgresqlDatabase
from datetime import datetime

s3_client = boto3.client('s3', region_name=AWS_REGION)
db = PostgresqlDatabase(PG_DB_NAME, user=PG_DB_USER, password=PG_DB_PWD, host=PG_DB_URL, port=PG_PORT)

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
    try:
        _ = s3_client.upload_file(file_name, bucket, object_name, ExtraArgs={'ContentType': 'text/plain; charset=utf-8'})
    except botocore.exceptions.ClientError as e:
        print(e)
        return False
    return True

def get_premium_user_list():
    local_premium_user_list = LOCAL_BASE_DIR + 'premium-user-list.csv'
    s3_client.download_file(S3_BUCKET_NAME, S3_PREMIUM_USER_LIST, local_premium_user_list)

    with open(local_premium_user_list, 'r') as f:
        lines = f.readlines()[1:]
        user_list = []
        for line in lines:
            split_line = line.strip().split(',')
            user = {
                'email': split_line[0],
                'premium_start': int(split_line[1]),
                'premium_end': int(split_line[2])
            }
            user_list.append(user)

    valid_users = []
    now = int(datetime.now().timestamp())
    for user in user_list:
        if user['premium_end'] > now:
            valid_users.append(user['email'])
        else:
            print('The user %s is not premium anymore.' % (user['email']))

    return valid_users

def connect_db():
    db.connect()

def disconnect_db():
    db.close()