import datetime
from typing import List

from src.config import DatabaseConfig
from src.model import User


class UserService:

    def __init__(self):
        self.db = DatabaseConfig()

    def select_user_list(self) -> List[User]:
        # 定义查询sql语句
        select_sql = 'SELECT * FROM open_idea_user WHERE username="lijunping"'
        # 接收查询结果
        query_result: List[User] = self.db.select_db(select_sql)
        print(query_result)
        return query_result

    def insert_user(self, user: User):
        # 定义查询sql语句
        sql = "INSERT INTO open_idea_user (username, create_time) VALUES ('%s', '%s');"
        time = str(datetime.datetime.now())
        data = (user.username, time)
        self.db.select_db(sql % data)
