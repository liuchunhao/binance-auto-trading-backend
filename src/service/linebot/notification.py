import requests
import os
import logging

from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s|%(levelname)-8s|%(message)s', datefmt='%Y%m%d %H:%M:%S')

token = os.getenv('LINE_TOKEN')

# 發送 Line 通知
def send_line_notify(message):
    # HTTP 標頭參數與資料
    headers = {"Authorization": f"Bearer {token}"}
    data = {"message": message}

    # 以 requests 發送 POST 請求
    requests.post("https://notify-api.line.me/api/notify", headers=headers, data=data)
    logging.info(f'send_line_notify: {message}')


