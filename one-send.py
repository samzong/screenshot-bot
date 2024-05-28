# /usr/bin/env python3
# -*- coding: UTF-8 -*-


"""

Author: samzong.lu
E-mail: samzong.lu@gmail.com

"""

from wecom import send_message

if __name__ == '__main__':
    pro_webhook_url = ''
    test_webhook_url = ''

    send_message(msy_type='text', message='管理决策透明化周报进度如下，请各位船员周知。', webhook=test_webhook_url)

    send_message(msy_type='image', message='2', webhook=test_webhook_url, image_file='1.png')
    send_message(msy_type='image', message='3', webhook=test_webhook_url, image_file='2.png')

