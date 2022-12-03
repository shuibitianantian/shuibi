import numpy as np

from calculation import prepare_data
from constants import COMPANY_INFO, MARKET_INFO, PROCESSED_DATA
from helper.DBHelper import DBHelper
import pandas as pd


def process_data(database_helper: DBHelper, code):
    hist = database_helper.execute(f"SELECT date, open, high, low, close, volume from {MARKET_INFO}"
                                   f" where symbol='{code}'")
    hist = pd.DataFrame(hist, columns=["date", 'open', 'high', 'low', 'close', 'volume'])
    hist['date'] = pd.to_datetime(hist.date, infer_datetime_format=False)
    return prepare_data(hist)


def update_dataset():
    db = DBHelper('shuibi')
    symbols = db.execute(f"SELECT symbol from {COMPANY_INFO}")

    try:
        db.execute(f"DROP TABLE {PROCESSED_DATA}")
        db.execute(f"""
            CREATE TABLE {PROCESSED_DATA} (
                date VARCHAR(255),
                open DOUBLE,
                high DOUBLE,
                low DOUBLE,
                close DOUBLE,
                volume DOUBLE,
                meanReturn DOUBLE,
                stdReturn DOUBLE,
                dDaySharpRatio DOUBLE,
                bbUp DOUBLE,
                bbMiddle DOUBLE,
                bbDown DOUBLE,
                aroonDown DOUBLE,
                aroonUp DOUBLE,
                ema12 DOUBLE,
                ema26 DOUBLE,
                label INT,
                symbol VARCHAR(255),
                PRIMARY KEY (symbol, date)
            )
        """)
    except Exception as e:
        print(e)

    for idx, (symbol, ) in enumerate(symbols):
        try:
            print(f"{idx + 1}/{len(symbols)} Update dataset of {symbol}")
            data = process_data(db, symbol)
            data.reset_index(drop=False, inplace=True)
            data.replace(np.nan, None, inplace=True)
            data['symbol'] = [symbol] * data.shape[0]
            db.insert_multiple(
                f"""
                    REPLACE INTO {PROCESSED_DATA} (date, open, high, low, close, volume, meanReturn, stdReturn,
                        dDaySharpRatio, bbUp, bbMiddle, bbDown, aroonDown, aroonUp, ema12, ema26, label, symbol
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                data.values.tolist())

        except Exception as e:
            print(e)
