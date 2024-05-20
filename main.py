import asyncio
import os
from datetime import datetime

import uvicorn
from apitable import Apitable
from fastapi import FastAPI
from fastapi.responses import RedirectResponse, FileResponse
from pydantic import BaseModel

from logger import get_logger
from record import handle_record
from screenshot import screenshot_for_url
from wecom import send_message

app = FastAPI()
logger = get_logger(__name__)

class DatasheetRequest(BaseModel):
    datasheet_id: str
    is_test: bool = False


# 创建一个锁来管理任务状态
lock = asyncio.Lock()

API_TOKEN = os.getenv("API_TOKEN")
API_BASE = os.getenv("APITABLE_BASE_URL")
apitable = Apitable(api_base=API_BASE, token=API_TOKEN)
product_webhook = os.getenv("WECOM_PROD_WEBHOOK")


def clean_cache_image():
    # 清理缓存图片
    for file in os.listdir():
        if file.endswith((".png", ".jpg")) and file.startswith(("1_", "2_", "3_")):
            os.remove(file)

async def task(datasheet_id: str, is_test: bool = False):
    # 获取数据表中的所有记录
    datasheet = apitable.datasheet(dst_id_or_url=datasheet_id, field_key="id")
    try:
        records = datasheet.records.all()
    except Exception as e:
        logger.error(f'An error occurred in datasheet.records.all(): {e}')
        return {"message": "获取数据表记录失败，确认是否可以访问 Apitable 数据表！"}

    # 通知产品群，周报任务开始了
    if is_test:
        # send_message(msy_type="text", message="日报任务发送开始！", webhook=product_webhook)
        pass

    # 循环执行每个记录
    try:
        for record in records:
            logger.info('%s >>> %s 发送开始', datetime.now().strftime('%Y-%m-%d %H:%M:%S'), record.json()['fldjtSK5iPPJ6'])
            handle_record(record)
            logger.info('%s <<< %s 发送完成', datetime.now().strftime('%Y-%m-%d %H:%M:%S'), record.json()['fldjtSK5iPPJ6'])
        if is_test:
            send_message(msy_type="text", message="日报任务发送完成！", webhook=product_webhook)

    except Exception as e:
        logger.error(f'An error occurred in handle_record: {e}')
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
        # 如果锁被占用，表示任务正在进行中
        return {"message": "周报统计任务进行中，请勿重复请求"}
    else:
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
        logger.error(f'An error occurred in test_screenshot: {e}')
        return f'An error occurred in screenshot_for_url: {e}, 截图失败！'


@app.get("/")
async def root():
    return RedirectResponse(url="/docs")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
