import datetime
import pytz
from constants import COMPANY_INFO, PROCESSED_DATA, PERFORMANCE
from helper.DBHelper import DBHelper


def get_symbols():
    db = DBHelper("shuibi")
    symbols = db.execute(f"SELECT symbol from {COMPANY_INFO}")
    del db
    return [symbol[0] for symbol in symbols]


def get_dataset(symbol):
    db = DBHelper("shuibi")
    data = db.execute(f"SELECT * from {PROCESSED_DATA} where symbol='{symbol}'")
    del db
    return data


def register_performance_data(performance):
    """
        This function helps to dump the performance data into database
        The performance data schema is:
            date string,
            model string,
            accuracy double,
            size int
    """

    db = DBHelper("shuibi")
    try:
        # db.execute(f"DROP TABLE {PERFORMANCE}")
        db.execute(
            f"""CREATE TABLE {PERFORMANCE} (
                    date VARCHAR(255),
                    model VARCHAR(255),
                    accuracy DOUBLE,
                    size INT,
                    PRIMARY KEY (date, model, size)
                ) ENGINE=INNODB;
            """)
    except Exception as e:
        print(e)

    if isinstance(performance, tuple):
        db.execute(f"REPLACE INTO {PERFORMANCE} VALUES ('{performance[0]}', '{performance[1]}', {performance[2]}, "
                   f"{performance[3]})")
    elif isinstance(performance, list):
        db.insert_multiple(f"REPLACE INTO {PERFORMANCE} VALUES (%s, %s, %s, %s)", performance)

    del db


def get_est_today_with_offset(offset=0):
    return str(datetime.datetime.utcnow().replace(tzinfo=pytz.timezone('US/Eastern')).date() - datetime.timedelta(days=offset))


if __name__ == '__main__':
    print(get_est_today_with_offset(3))

