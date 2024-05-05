# /usr/bin/env python3
# -*- coding: UTF-8 -*-


"""

Author: samzong.lu
E-mail: samzong.lu@gmail.com

https://apitable.daocloud.io/workbench/dstrqpMc5uCrC8lWge

fldjtSK5iPPJ6 客户名称
fldJAgnhUjLNf 关联项目
flduoxSXPabw6 项目所属区域
fld4yMzYbuxq0 发送频次
fldOcS36Ww4hx 企业微信群名
fldJqbySNwota 群机器人链接
fldwoUisE6688 分享文件夹链接
fldB5J4474Pyl 消息内容

"""

import time
import logging
from datetime import datetime
from chinese_calendar import is_workday

from wecom_msg import send_message
from screenshot import screenshot

# 今天星期几
today_of_weekday = datetime.now().weekday()
# 今天是本月份的第几天
today_of_month = datetime.now().day

# 判断今天是不是中国法定工作日
is_china_workday = is_workday(datetime.now())


def handle_record(record):
    # 判断今天是否为工作日
    if not is_china_workday:
        print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ", 今天是不是法定工作日")
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ", 今天是不是法定工作日"

    if record.fldJqbySNwota and record.fldwoUisE6688 and record.fldB5J4474Pyl:
        print(datetime.now().strftime(
            '%Y-%m-%d %H:%M:%S'), "数据内容：", record.json())

        project_name = record.json()['fldjtSK5iPPJ6']  # 客户名称
        wecom_bot_url = record.json()['fldJqbySNwota']  # 群机器人链接
        share_folder_url = record.json()['fldwoUisE6688']  # 分享文件夹链接
        wecom_message = record.json()['fldB5J4474Pyl']  # 消息内容

        try:
            # 截图
            snapshot = screenshot(
                url=share_folder_url, screenshot_name=project_name + "_screenshot.png")

            # 发送消息
            send_message(msy_type="text", message=wecom_message,
                         webhook=wecom_bot_url)
            if snapshot and len(snapshot) > 0:
                for image in snapshot:
                    send_message(msy_type="image", message=wecom_message,
                                 webhook=wecom_bot_url, image_file=image)
            # 发送机器人提醒
            send_message(
                msy_type="text", message=f"本周报由产品助手机器人发送，详情请查看 {share_folder_url}, 若数据有疑问，请在群里联系负责产品经理。", webhook=wecom_bot_url)
        except Exception as e:
            logging.error(f'An error occurred: {e}')
        finally:
            print(datetime.now().strftime(
                '%Y-%m-%d %H:%M:%S'), "项目发送结束", record.json())
            time.sleep(10)


if __name__ == '__main__':
    pass
