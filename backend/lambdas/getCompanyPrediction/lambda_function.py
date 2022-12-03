
from constants import PREDICTION
import json
import boto3
from decouple import AutoConfig
import os
from pathlib import Path
import datetime
import pytz

DOTENV_FILE = os.path.join(Path(__file__).parent.absolute(), '.env')
config = AutoConfig(search_path=DOTENV_FILE)

BUCKET = config('BUCKET')
KEY = config('AWS_ACCESS_KEY_ID')
SECRET = config('AWS_SECRET_KEY')


def get_est_today_with_offset(offset=0):
    return str(datetime.datetime.utcnow().replace(tzinfo=pytz.timezone('US/Eastern')).date() - datetime.timedelta(days=offset))


def lambda_handler(event, context):
    yesterday = get_est_today_with_offset(1)
    symbol = json.loads(event["body"])["symbol"]

    if not symbol:
        return {
            "statusCode": 401,
            "body": "Unrecognized request"
        }

    s3 = boto3.client('s3')
    resp = s3.select_object_content(
        Bucket=BUCKET,
        Key=f'tables/{PREDICTION}-{yesterday}.csv',
        ExpressionType='SQL',
        Expression=f"SELECT * FROM s3object s where s.\"symbol\" = '{symbol}' and s.\"date\"='{yesterday}'",
        InputSerialization={'CSV': {"FileHeaderInfo": "Use"}, 'CompressionType': 'NONE'},
        OutputSerialization={'JSON': {}},
    )

    results = []
    for event in resp['Payload']:
        if "Records" in event:
            record = event["Records"]['Payload'].decode('utf-8')
            results.append(record)

    return {
        "statusCode": 200,
        "body": json.dumps(results)
    }

