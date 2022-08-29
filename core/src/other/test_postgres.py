import psycopg2
import os

try:
    connection = psycopg2.connect(user = "postgres",
                                  password = os.environ['PG_DB_PWD'],
                                  host = os.environ['PG_DB_URL'],
                                  port = "5432",
                                  database = "postgres")
    print("Successfully connected!")
except (Exception, psycopg2.Error) as error :
    print ("Error while connecting to PostgreSQL", error)