import datetime
import json
from typing import Optional, TypeVar, Generic, List
import uvicorn
from fastapi import FastAPI, Request as HttpRequest
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from src.model import User
from src.service import UserService

T = TypeVar('T')


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        if isinstance(obj, int):
            return int(obj)
        elif isinstance(obj, float):
            return float(obj)
        else:
            return super(CustomEncoder, self).default(obj)


class ServerException(Exception):
    # 初始化
    def __init__(self, message):
        self.message = message

    # 类一般返回值
    def __str__(self):
        return "服务异常:" + self.message


class Request(BaseModel):
    title: str
    page: int = 1


class Result(BaseModel, Generic[T]):
    code: int = 200
    msg: str = "success"
    data: T = None

    def success(self, data: T):
        self.code = 200
        self.msg = "success"
        self.data = data

    def error(self, msg: str):
        self.code = 1000
        self.msg = msg
        self.data = None


server = FastAPI()

server.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


@server.get("/test")
def read_root():
    return {"Hello": "World"}


@server.post('/query', response_model=Result)
async def query(request: Request):
    title = request.title
    page = request.page

    print(f'Hi, {title}, {page}')

    result = Result[str]()
    result.success(data=title)

    return result


@server.post('/api', response_model=Result)
async def query(request: Request):
    title = request.title
    page = request.page

    print(f'Hi, {title}, {page}')
    result = Result[str]()

    try:
        res = 10 / page
        print(f'结果， {res}')
        result.success(data=title)
    except Exception as e:
        # print(e)
        # result.error(str(e))
        raise ServerException(str(e))

    return result


@server.get("/getUser")
async def get_user():
    try:
        user_service = UserService()
        query_result: List[User] = user_service.select_user_list()
        result = Result()
        result.success(data=query_result)
        return result
    except Exception as e:
        raise ServerException(str(e))


@server.post("/createUser")
async def create_user(user: User):
    try:
        user_service = UserService()
        user_service.insert_user(user)
        result = Result()
        result.success(data=None)
        return result
    except Exception as e:
        raise ServerException(str(e))


@server.exception_handler(ServerException)
async def exception_handler(request: HttpRequest, exc: ServerException):
    print(f"服务异常：{request.method} {request.url}")
    print(exc)
    result = Result()
    result.error(exc.message)
    print(type(result))  # result 是个对象
    # 直接 return JSONResponse(content=result) 或 return JSONResponse(content=json.dumps(result)) 都会报错
    # 报 TypeError: Object of type Result is not JSON serializable，
    # 我们这里先把响应结果转为json，再去格式化响应内容。
    # 这里最终转为 dict 返回
    return JSONResponse(content=json.loads(result.json()))


# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # print_hi('OpenByteCode')
    # server.run(debug=True, threaded=True)
    uvicorn.run(app=server, host="localhost", port=8080, workers=1)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
