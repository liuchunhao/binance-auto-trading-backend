import requests

from service.binance import binance_bot_get_signed_request
from config import TOKEN 


def send_line_notify(message):
    # HTTP 標頭參數與資料
    headers = {"Authorization": f"Bearer {TOKEN}"}
    data = {"message": message}

    # 以 requests 發送 POST 請求
    requests.post("https://notify-api.line.me/api/notify", headers=headers, data=data)


def main():
    account_snapshot = binance_bot_get_signed_request.get_account_snapshot()
    print(account_snapshot)
    # send_line_notify(account_snapshot)


if __name__ == '__main__':
    main()
