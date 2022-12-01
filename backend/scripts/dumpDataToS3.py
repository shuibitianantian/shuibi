"""
Need to upload companyInfo table, prediction table
"""
import datetime
from helper.DBHelper import DBHelper
from constants import COMPANY_INFO
import pandas as pd
import boto3
from decouple import AutoConfig
import os
from pathlib import Path

DOTENV_FILE = os.path.join(Path(__file__).parent.absolute(), '.env')
config = AutoConfig(search_path=DOTENV_FILE)

KEY = config('AWS_ACCESS_KEY_ID')
SECRET = config('AWS_SECRET_KEY')
BUCKET = config('BUCKET')
TARGET_TABLES = [COMPANY_INFO]


def generate_file_name(table_name):
    today = str(datetime.date.today())
    return f'{table_name}-{today}.csv'


def dump_data():
    db = DBHelper('shuibi')
    for table in TARGET_TABLES:
        print(f"Dump table {table}.")
        results = db.execute(f"SELECT * from {table}")
        columns = db.execute(f"SHOW COLUMNS from {table}")
        df = pd.DataFrame(results, columns=[col[0] for col in columns])
        df.to_csv(f'../data/{generate_file_name(table)}')


def upload_file_to_s3():
    s3 = boto3.resource('s3', aws_access_key_id=KEY, aws_secret_access_key=SECRET)
    for table in TARGET_TABLES:
        file_name = generate_file_name(table)
        file_full_path = f'../data/{file_name}'
        try:
            s3.Bucket(BUCKET).upload_file(file_full_path, f"tables/{file_name}")
        except Exception as e:
            print(e)


if __name__ == '__main__':
    dump_data()
    upload_file_to_s3()

