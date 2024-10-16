from service.binance import user_data
from service.linebot import notification

if __name__ == '__main__':
    resp = user_data.get_yesterday_funding_fee_sum('BTCUSDT')
    print(resp)
    notification.send_line_notify(resp)

    resp = user_data.get_yesterday_funding_fee_sum('BNBUSDT')
    print(resp)
    notification.send_line_notify(resp)
