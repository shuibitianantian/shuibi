import json

import boto3
from decouple import AutoConfig
import os
from pathlib import Path
import datetime
from constants import COMPANY_INFO
import pytz

DOTENV_FILE = os.path.join(Path(__file__).parent.absolute(), '.env')
config = AutoConfig(search_path=DOTENV_FILE)

BUCKET = config('BUCKET')
KEY = config('AWS_ACCESS_KEY_ID')
SECRET = config('AWS_SECRET_KEY')


def get_est_today_with_offset(offset=0):
    return str(
        datetime.datetime.utcnow().replace(tzinfo=ZoneInfo('US/Eastern')).date() - datetime.timedelta(days=offset))


def lambda_handler(event, context):
    yesterday = get_est_today_with_offset(1)
    s3 = boto3.client('s3')
    resp = s3.select_object_content(
        Bucket=BUCKET,
        Key=f'tables/{COMPANY_INFO}-{yesterday}.csv',
        ExpressionType='SQL',
        Expression="SELECT * FROM s3object s",
        InputSerialization={'CSV': {"FileHeaderInfo": "Use"}, 'CompressionType': 'NONE'},
        OutputSerialization={'JSON': {}},
    )

    results = ''
    for event in resp['Payload']:
        if "Records" in event:
            results += event["Records"]['Payload'].decode('utf-8')

    results = [json.loads(row) for row in results.split('\n') if row]

    return {
        "statusCode": 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        "body": json.dumps(results)
    }