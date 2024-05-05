# /usr/bin/env python3
# -*- coding: UTF-8 -*-


"""

Author: samzong.lu
E-mail: samzong.lu@gmail.com

"""
import requests
import hashlib
import base64
from compress import compress_image


def get_image_md5_base64(image_path):
    with open(image_path, 'rb') as f:
        data = f.read()

    # Calculate MD5
    md5_hash = hashlib.md5(data).hexdigest()

    # Calculate Base64
    base64_data = base64.b64encode(data).decode('utf-8')

    return md5_hash, base64_data


def text_message(message: str):
    return {
        "msgtype": "text",
        "text": {
            "content": message
        }
    }


def image_message(image_file: str):
    # 企业微信不允许发送超过 2MB 的图片，超过需要压缩
    image_file = compress_image(image_file, mb=2)

    md5_data, base64_data = get_image_md5_base64(image_path=image_file)

    return {
        "msgtype": "image",
        "image": {
            "base64": base64_data,
            "md5": md5_data
        }
    }


def send_message(msy_type: str, message: str, webhook: str, image_file: str = None):
    if msy_type == 'text':
        requests.post(url=webhook, json=text_message(message=message))
    elif msy_type == 'image':
        requests.post(url=webhook, json=image_message(image_file=image_file))


if __name__ == '__main__':
    send_message(
        msy_type="image",
        message="测试消息",
        webhook="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=3fd6fa58-b5ac-41b6-8f7e-0e0c26931d65",
        image_file="3_富国 screenshot.png"
    )
