import pymysql
import configparser
from pymysql.cursors import DictCursor

config_path = 'D:/project/open/Open-AI/Python-Web-Demo/src/config.ini'


class DatabaseConfig:
    def __init__(self):
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
        # 以字典形式返回结果的游标
        self.cursor = self.connect.cursor(cursor=pymysql.cursors.DictCursor)

    def __del__(self):  # 对象资源被释放时触发，在对象即将被删除时的最后操作
        # 关闭游标
        self.cursor.close()
        # 关闭数据库连接
        self.connect.close()

    def select_db(self, sql: str):
        """
        查询操作
        :param sql: 传入查询sql语句
        :return: 返回查询结果
        """

        # 使用 execute() 执行sql
        self.cursor.execute(sql)

        # 使用 fetchall() 获取查询结果
        data = self.cursor.fetchall()
        # 返回查询数据
        return data

    def change_db(self, sql: str):
        """
        变更数据操作----更新/插入/删除
        :param sql: 传入数据库语句
        :return: 没有返回值
        """

        try:
            # 使用 execute() 执行sql
            self.cursor.execute(sql)
            # 提交事务
            self.connect.commit()
        except Exception as e:
            print("操作出现错误：{}".format(e))
            # 回滚所有更改
            self.connect.rollback()
