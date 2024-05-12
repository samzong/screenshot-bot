import asyncio
import os

from apitable import Apitable
from fastapi import FastAPI
from fastapi.responses import RedirectResponse, FileResponse
from pydantic import BaseModel

from auto_msg_and_image import handle_record
from screenshot import screenshot_for_url
from wecom_msg import send_message

app = FastAPI()


class DatasheetRequest(BaseModel):
    datasheet_id: str
    is_test: bool = False


# 创建一个锁来管理任务状态
lock = asyncio.Lock()

API_TOKEN = os.getenv("API_TOKEN")
apitable = Apitable(api_base="https://apitable.daocloud.io", token=API_TOKEN)
product_webhook = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=eab79c07-e732-4d93-b5c9-842a1051f890"


async def task(datasheet_id: str, is_test: bool = False):
    # 获取数据表中的所有记录
    datasheet = apitable.datasheet(dst_id_or_url=datasheet_id, field_key="id")
    records = datasheet.records.all()

    # 通知产品群，周报任务开始了
    if is_test:
        send_message(msy_type="text", message="日报任务发送开始！", webhook=product_webhook)

    # 循环执行每个记录
    try:
        for record in records:
            handle_record(record)
        if is_test:
            send_message(msy_type="text", message="日报任务发送完成！", webhook=product_webhook)

    except Exception as e:
        print(f'An error occurred: {e}')
    finally:
        # 只有在锁被获取的情况下才尝试释放锁
        if lock.locked():
            lock.release()

def gen_datasheet_field(datasheet_id: str):
    datasheet = apitable.datasheet(dst_id_or_url=datasheet_id, field_key="id")
    return datasheet.fields.all()


@app.post("/start_task", tags=["task"], summary="启动任务", description="启动周报统计任务")
async def start_task(request: DatasheetRequest):
    datasheet_id = request.datasheet_id
    is_test = request.is_test
    if lock.locked():
        print("11111")
        # 如果锁被占用，表示任务正在进行中
        return {"message": "周报统计任务进行中，请勿重复请求"}
    else:
        print("22222")
        # 尝试获取锁并启动任务
        await lock.acquire()
        asyncio.create_task(task(datasheet_id=datasheet_id, is_test=is_test))
        return {"message": "周报统计任务已开始"}


@app.post("/datasheet_field", tags=["task"], summary="获取数据表字段", description="获取数据表字段")
async def datasheet_field(request: DatasheetRequest):
    return gen_datasheet_field(datasheet_id=request.datasheet_id)


@app.get("/test-screenshot", tags=["test"], summary="测试截图功能", description="提供任意一个链接测试截图功能是否正常")
async def test_sreenshot():
    try:
        if screenshot_for_url(url="https://www.baidu.com", screenshot_name="baidu.png"):
            return FileResponse("baidu.png", media_type="image/png")
    except Exception as e:
        return f'An error occurred: {e}, 截图失败！'


@app.get("/")
async def root():
    return RedirectResponse(url="/docs")
