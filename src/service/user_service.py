from src.config import DatabaseConfig


class UserService:

    def __init__(self):
        self.db = DatabaseConfig()

    def select_user_list(self):
        # 定义查询sql语句
        select_sql = 'SELECT * FROM open_idea_user WHERE username="lijunping"'
        # 接收查询结果
        query_result = self.db.select_db(select_sql)
        print(query_result)
        return query_result
