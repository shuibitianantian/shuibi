"""
We get the list of stock code from wikipedia
"""
import numpy as np
import pandas as pd

from constants import COMPANY_INFO, STOCKS_LIST_URL, DB_NAME
from helper.DBHelper import DBHelper


def update_company_info():
    stock_code_tabel = pd.read_html(STOCKS_LIST_URL)[0][['Symbol', 'Security', 'GICS Sector', 'GICS Sub-Industry',
                                                         'Headquarters Location', 'Date first added', 'CIK', 'Founded']]
    stock_code_tabel.fillna(value="")
    db_helper = DBHelper(DB_NAME)

    try:
        db_helper.execute(f"DROP TABLE {COMPANY_INFO}")
    except Exception as e:
        print(e)

    db_helper.execute(
        f"""
            CREATE TABLE {COMPANY_INFO} (
                symbol VARCHAR(255) PRIMARY KEY,
                security VARCHAR(255),
                sector VARCHAR(255),
                subIndustry VARCHAR(255),
                headquarterLocation VARCHAR(255),
                added VARCHAR(255),
                cik VARCHAR(255),
                founded VARCHAR(255)
            ) ENGINE=INNODB;
        """
    )

    number_of_records_to_insert = len(stock_code_tabel.values.tolist())
    print(f"Inserting {number_of_records_to_insert} records into {COMPANY_INFO}")
    # inserting company information into table
    stock_code_tabel = stock_code_tabel.replace(np.nan, None)
    db_helper.insert_multiple(f"""
            INSERT INTO {COMPANY_INFO} VALUES
            (%s, %s, %s, %s, %s, %s, %s, %s)
        """, stock_code_tabel.values.tolist())
    number_of_records_found = db_helper.execute(f"select count(*) from {COMPANY_INFO}")[0]

    assert number_of_records_found[0] == number_of_records_to_insert, \
        f"Numbers not matched, {number_of_records_to_insert} to insert, but {number_of_records_found[0]} found"

    print(f"{COMPANY_INFO} updated successfully")

