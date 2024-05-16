# /usr/bin/env python3
# -*- coding: UTF-8 -*-


"""

Author: samzong.lu
E-mail: samzong.lu@gmail.com

fldjtSK5iPPJ6 客户名称
fldJAgnhUjLNf 关联项目
flduoxSXPabw6 项目所属区域
fld4yMzYbuxq0 发送频次
fldOcS36Ww4hx 企业微信群名
fldJqbySNwota 群机器人链接
fldwoUisE6688 分享文件夹链接
fldB5J4474Pyl 消息内容

"""

import logging
import time
from datetime import datetime

from chinese_calendar import is_workday

from logger import get_logger
from screenshot import screenshot
from wecom import (send_message)

logger = get_logger(__name__)

# 今天星期几
today_of_weekday = datetime.now().weekday()
# 今天是本月份的第几天
today_of_month = datetime.now().day

# 判断今天是不是中国法定工作日
is_china_workday = is_workday(datetime.now())


def _handle_trigger(project_name: str, wecom_bot_url: str, share_folder_url: str, wecom_message: str):
    try:
        # 执行截图动作
        snapshot = screenshot(url=share_folder_url, screenshot_name=project_name + ".png")

        # 发送开始消息
        send_message(msy_type="text", message=wecom_message, webhook=wecom_bot_url)

        # 发送图片消息
        if snapshot and len(snapshot) > 0:
            for image in snapshot:
                send_message(msy_type="image", message=wecom_message, webhook=wecom_bot_url, image_file=image)

        # 发送结束提示语
        send_message(
            msy_type="text", message=f"报告由助手自动发送，详情查看 {share_folder_url}； 若有疑问，在群里联系负责产品经理。", webhook=wecom_bot_url)

    except Exception as e:
        logging.error(f'An error occurred in send_message: {e}')

    finally:
        time.sleep(10)  # 休息10秒


def handle_record(record):
    _current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    fields = ['fldjtSK5iPPJ6', 'fldJqbySNwota', 'fldwoUisE6688', 'fldB5J4474Pyl', 'fld4yMzYbuxq0']
    record_json = record.json()

    if not all(field in record_json for field in fields):
        logger.warning(_current_time + ", 项目信息不完整")
        return _current_time + ", 项目信息不完整"

    if not all(record_json.get(field) for field in fields):
        logger.warning(_current_time + ", 存在字段值为空")
        return _current_time + ", 存在字段值为空"

    # 初始化参数
    project_name = record.json()['fldjtSK5iPPJ6']  # 客户名称
    wecom_bot_url = record.json()['fldJqbySNwota']  # 群机器人链接
    share_folder_url = record.json()['fldwoUisE6688']  # 分享文件夹链接
    wecom_message = record.json()['fldB5J4474Pyl']  # 消息内容
    send_frequency = record.json()['fld4yMzYbuxq0']  # 发送频次

    # 判断今天是否为工作日，非工作日，不执行发送计划
    if not is_china_workday:
        logger.warning(_current_time + ", 今天不是法定工作日")
        return _current_time + ", 今天不是法定工作日"

    # 周一发送，如果不是周一不发送
    if send_frequency == "每周一次" and today_of_weekday == 0:
        _handle_trigger(project_name, wecom_bot_url, share_folder_url, wecom_message)
        return _current_time + ", 每周发送，今天是周一，发送成功"

    # 发送每日报告
    if send_frequency == "每日":
        _handle_trigger(project_name, wecom_bot_url, share_folder_url, wecom_message)
        return _current_time + ", 每日发送，发送成功"
