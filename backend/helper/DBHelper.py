"""
Design: 

1. The helper should use a global configuration to connect the database
2. The helper should be able to dump data into database
3. The helper should be able to run SQL to get data from database

We use `sqlalchemy` to connect database
"""
from decouple import config, AutoConfig
from mysql import connector
from pathlib import Path
import os

DOTENV_FILE = os.path.join(Path(__file__).parent.absolute(), '.env')
AutoConfig(search_path=DOTENV_FILE)

HOSTNAME = config('hostname')
USERNAME = config('uname')
PASSCODE = config('pwd')


class DBHelper:
    def __init__(self, database: str) -> None:
        self.conn = connector.connect(
            host=HOSTNAME,
            user=USERNAME,
            password=PASSCODE,
        )

        assert self.conn is not None, "Database connection is not established!"

        self._initialize_database(database)

    def _initialize_database(self, database):
        cursor = self.conn.cursor()
        cursor.execute(f'CREATE DATABASE IF NOT EXISTS {database}')
        cursor.close()
        self.conn.close()
        self.conn = connector.connect(
            host=HOSTNAME,
            user=USERNAME,
            password=PASSCODE,
            database=database
        )

    def __del__(self):
        self.conn.close()

    def execute(self, sql, *args):
        cursor = self.conn.cursor()
        cursor.execute(sql, args)
        results = cursor.fetchall()
        self.conn.commit()
        cursor.close()
        return results

    def insert_multiple(self, query, data):
        cursor = self.conn.cursor()
        cursor.executemany(query, data)
        self.conn.commit()
        cursor.close()
