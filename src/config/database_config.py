import pymysql
import configparser
from typing import List, Tuple


class DatabaseConfig:
    def __init__(self, config_path: str):
        # 获取emb_url
        self.config = configparser.ConfigParser()
        self.config.read(config_path, encoding='utf-8')
        self.connect = pymysql.connect(
            host=self.config.get('database', 'host'),
            port=int(self.config.get('database', 'port')),
            user=self.config.get('database', 'user'),
            password=self.config.get('database', 'password'),
            database=self.config.get('database', 'database'),
            charset=self.config.get('database', 'charset')
        )
        self.cursor = self.connect.cursor()

    def insert_right_feedback(self, sql_text, data):
        self.cursor.execute(sql_text % data)
        self.connect.commit()

    def insert_wrong_feedback(self, sql_text):
        self.cursor.execute(sql_text)
        self.connect.commit()

    def select_feedback(self, sql_text: str) -> Tuple:
        self.cursor.execute(sql_text)
        result = self.cursor.fetchall()
        return result

    def close(self):
        self.cursor.close()
        self.connect.close()
