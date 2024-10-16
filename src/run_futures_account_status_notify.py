from service.binance import user_data
from service.linebot import notification

if __name__ == '__main__':
    totalMarginBalance, margin, resp = user_data.get_futures_account_status()
    print(f'totalMarginBalance: {totalMarginBalance}')
    notification.send_line_notify(resp)
