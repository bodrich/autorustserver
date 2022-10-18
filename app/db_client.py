import functools
import sqlite3
from datetime import datetime
from typing import Any

from app.config import settings


class DBClient:
    GET_LAST_WIPE_SQL = """SELECT wipe_timestamp FROM wipes order by wipe_timestamp desc limit 1"""
    GET_LAST_REBOOT_SQL = """SELECT reboot_timestamp FROM reboots order by reboot_timestamp desc limit 1"""
    INSERT_WIPE_TIMESTAMP_SQL = """INSERT INTO wipes(wipe_timestamp)  VALUES(datetime())"""
    INSERT_REBOOT_TIMESTAMP_SQL = """INSERT INTO reboots(reboot_timestamp)  VALUES(datetime())"""

    def __init__(self, file_name: str = settings.SQLITE_FILE_NAME):
        self.db_file_name: str = file_name
        self.sqlite_connection: sqlite3.Connection = None
        self.cursor: sqlite3.Cursor = None

    def _make_new_connection(self):
        self.sqlite_connection: sqlite3.Connection = sqlite3.connect(self.db_file_name)
        self.cursor: sqlite3.Cursor = self.sqlite_connection.cursor()

    def _close_connection(self):
        self.sqlite_connection.commit()
        self.sqlite_connection.close()

    # todo: раскоментить на питоне 3.10
    #@staticmethod
    def new_connection(func):
        @functools.wraps(func)
        def wrapper(instance, *args, **kwargs):
            result: Any = None
            try:
                instance._make_new_connection()
                result = func(instance, *args, **kwargs)
            finally:
                instance._close_connection()
            return result
        return wrapper

    def _get_last_time_from_sql(self, sql_raw_query: str) -> datetime:
        self.cursor.execute(sql_raw_query)
        record = self.cursor.fetchone()
        if not record:
            return datetime.utcfromtimestamp(0)
        return datetime.strptime(record[0], '%Y-%m-%d %H:%M:%S')

    @new_connection
    def get_last_wipe(self) -> datetime:
        return self._get_last_time_from_sql(self.GET_LAST_WIPE_SQL)

    @new_connection
    def get_last_reboot(self) -> datetime:
        return self._get_last_time_from_sql(self.GET_LAST_REBOOT_SQL)

    @new_connection
    def insert_wipe_timestamp(self):
        self.cursor.execute(self.INSERT_WIPE_TIMESTAMP_SQL)
        self.cursor.fetchall()

    @new_connection
    def insert_reboot_timestamp(self):
        self.cursor.execute(self.INSERT_REBOOT_TIMESTAMP_SQL)
        self.cursor.fetchall()
