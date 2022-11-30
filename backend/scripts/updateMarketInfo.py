"""
Steps:
1. if the marketInfo table does not exist, we fetch stock prices of last 5 years.
2. if the marketInfo table exist, we fetch today's price for all company.
3. Schedule this job to run every day.
"""
import time

import mysql.connector.errors
import numpy as np
from constants import DB_NAME, MARKET_INFO, COMPANY_INFO
from helper.DBHelper import DBHelper
import yfinance as yf


def update_market_info():
    db_helper = DBHelper(DB_NAME)

    company_symbols = db_helper.execute(f"SELECT symbol FROM {COMPANY_INFO}")

    # # Drop the table will cause the program always fetch max data
    # db_helper.execute(f"DROP TABLE {MARKET_INFO}")

    try:
        db_helper.execute(f"select * from {MARKET_INFO}")
        is_init = False
    except mysql.connector.errors.ProgrammingError as e:
        if f"'shuibi.{MARKET_INFO.lower()}' doesn't exist" in str(e):
            db_helper.execute(
                f"""
                    CREATE TABLE {MARKET_INFO} (
                        date VARCHAR(255),
                        open DOUBLE,
                        high DOUBLE,
                        low DOUBLE,
                        close DOUBLE,
                        volume DOUBLE,
                        dividends DOUBLE,
                        stockSplits DOUBLE,
                        symbol VARCHAR(255),
                        PRIMARY KEY (symbol, date)
                    ) ENGINE=INNODB;
                """)
        is_init = True

    unhandled_companies = []
    for idx, row in enumerate(company_symbols):
        symbol = row[0]
        try:
            print(f'{idx + 1}/{len(company_symbols)} Updating marget info for {symbol}.')
            stock = yf.Ticker(symbol)
            hist = stock.history(period='max' if is_init else '1d')
            hist.reset_index(drop=False, inplace=True)
            hist['symbol'] = [symbol] * hist.shape[0]
            hist = hist.replace(np.nan, None)

            db_helper.insert_multiple(
                f"""
                    INSERT INTO {MARKET_INFO} 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, hist.values.tolist()
            )

            time.sleep(0.5)
        except Exception as e:
            print(f"{symbol}: {e}")
            unhandled_companies.append(symbol)