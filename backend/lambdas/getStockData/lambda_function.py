import json
import requests

HEADERS = {
    'Connection': 'keep-alive',
    'Expires': '-1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'
}


def build_query(symbol):
    return f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"


def lambda_handler(event, body):
    symbol = json.loads(event['body'])['symbol']
    query = build_query(symbol)
    result = requests.get(query, headers=HEADERS)
    print(len(json.loads(result.text)['chart']['result'][0]['indicators']['quote'][0]['open']))

    return {
        "statusCode": 200,
        "body": json.dumps({})
    }

lambda_handler({"body": "{\"symbol\": \"AAPL\"}"}, None)
