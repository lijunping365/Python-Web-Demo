from typing import Optional, TypeVar, Generic
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

T = TypeVar('T')


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
        print(e)
        result.error("未知错误")

    return result


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
