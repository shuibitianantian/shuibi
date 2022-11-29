"""
We get the list of stock code from wikipedia
"""
import pandas as pd

from constants import COMPANY_INFO
from helper.DBHelper import DBHelper

STOCKS_LIST_URL = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

stock_code_tabel = pd.read_html(STOCKS_LIST_URL)[0][['Symbol', 'Security', 'GICS Sector', 'GICS Sub-Industry',
                                                     'Headquarters Location', 'Date first added', 'CIK', 'Founded']]

stock_code_tabel.fillna(value="")

dbHelper = DBHelper('shuibi')
dbHelper.execute(f"DROP TABLE {COMPANY_INFO}")

dbHelper.execute(
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

for info in stock_code_tabel.values.tolist():
    dbHelper.execute(f"""
        INSERT INTO {COMPANY_INFO} VALUES
         ("{info[0]}", "{info[1]}", "{info[2]}", "{info[3]}", "{info[4]}", "{info[5]}", "{info[6]}", "{info[7]}")
    """, )
number_of_records_found = dbHelper.execute(f"select count(*) from {COMPANY_INFO}")[0]

assert number_of_records_found[0] == number_of_records_to_insert, \
    f"Numbers not matched, {number_of_records_to_insert} to insert, but {number_of_records_found[0]} found"

print(f"{COMPANY_INFO} updated successfully")
