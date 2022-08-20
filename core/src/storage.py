import boto3
import botocore
from constants import AWS_REGION, S3_SQLITE_DB_BASE_DIR, BASE_SQLITE_DB_FILE, LOCAL_BASE_DIR, S3_BUCKET_NAME
from os.path import exists
from pyliquibase import Pyliquibase
from peewee import SqliteDatabase

s3_client = boto3.client('s3', region_name=AWS_REGION)
db = SqliteDatabase(LOCAL_BASE_DIR + BASE_SQLITE_DB_FILE, pragmas={
    'journal_mode': 'wal',  # WAL-mode.
    'cache_size': -64 * 1000,  # 64MB cache.
    })

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
        _ = s3_client.upload_file(file_name, bucket, object_name, ExtraArgs={'ACL': 'public-read', 'ContentType': 'text/plain; charset=utf-8'})
    except botocore.exceptions.ClientError as e:
        print(e)
        return False
    return True

def sync_db():
    """Synchronize database with S3 buckets by local first priority

    :return: True if sync succeeded, else False
    """

    sqlite_local_file_name = LOCAL_BASE_DIR + BASE_SQLITE_DB_FILE
    sqlite_s3_file_name = S3_SQLITE_DB_BASE_DIR + BASE_SQLITE_DB_FILE
    if (exists(sqlite_local_file_name)):
        print("Uploading database to S3...")
        try:
            _ = s3_client.upload_file(sqlite_local_file_name, S3_BUCKET_NAME, sqlite_s3_file_name)
        except botocore.exceptions.ClientError as e:
            print(e)
            return False
    else:
        # Download database from S3
        print("Download database from S3...")
        try:
            _ = s3_client.download_file(S3_BUCKET_NAME, sqlite_s3_file_name, sqlite_local_file_name)
        except botocore.exceptions.ClientError as e:
            print(e)
            return False
    return True

def do_db_migration():
    liquibase = Pyliquibase(defaultsFile="db/liquibase.properties")
    liquibase.update()

def connect_db():
    db.connect()

def disconnect_db():
    db.close()