# /usr/bin/env python3
# -*- coding: UTF-8 -*-


"""

Author: samzong.lu
E-mail: samzong.lu@gmail.com

"""

from wecom import send_message

if __name__ == '__main__':
    webhook_url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=9ea86765-90e7-47a7-8e73-2bafb060a24c'

    send_message(msy_type='text', message='管理决策透明化周报进度如下，请各位船员周知。', webhook=webhook_url)

    send_message(msy_type='image', message='2', webhook=webhook_url, image_file='1.png')
    send_message(msy_type='image', message='3', webhook=webhook_url, image_file='2.png')

