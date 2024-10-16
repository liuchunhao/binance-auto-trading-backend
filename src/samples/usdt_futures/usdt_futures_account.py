import requests
import time
import hmac
import hashlib
import json
import service.linebot.line_notify_bot as line_notify_bot

API_KEY = '1XHbm0oQXt0ocT4NlSEsejfyLhnErejQXqcOxGdVTAE1I0XyZNgkdXFhF4ojmksw'
SECRET_KEY = b'O7F7iXmMKFhXLwwIPfhKBMxo9yOsD5GjmgafzYEkMoDvK4C13PbqF7ei2qCmGT1c'

timestamp = int(time.time() * 1000)
params = {'timestamp': timestamp}
query_string = '&'.join([f'{k}={v}' for k, v in params.items()])
print()
signature = hmac.new(SECRET_KEY, query_string.encode('utf-8'), hashlib.sha256).hexdigest()

headers = {
    'Content-Type': 'application/json',
    'X-MBX-APIKEY': API_KEY
}

def render_epoch_time(epoch_time):
    import datetime
    epoch_time = epoch_time / 1000  # convert miliseconds to seconds
    human_time = datetime.datetime.fromtimestamp(epoch_time).strftime('%Y-%m-%d %H:%M:%S')
    return human_time


# 帳戶信息: https://binance-docs.github.io/apidocs/futures/cn/#v2-user_data
def get_account(margin=8000):
    url = 'https://fapi.binance.com/fapi/v2/account'
    response = requests.get(url, headers=headers, params={
        'timestamp': timestamp,
        'signature': signature
    })

    # print(response)
    # print(json.dumps(response.json(), indent=4))

    res = response.json()
    total_wallet_balance = res['totalWalletBalance']
    total_unrealized_profit = res['totalUnrealizedProfit']
    total_margin_balance = res['totalMarginBalance']
    s = []
    assets = res['assets']
    for asset in assets: 
        ast = asset['asset']
        if ast == 'USDT':
            margin_balance = float(asset['marginBalance'])
            if margin_balance < margin:
                s.append("通知: 測試, 不要緊張")
                s.append(f'保證金餘額 < {margin}')
                s.append("資產:")
                s.append(f"asset: {ast}")
                s.append(f"保證金餘額:  {asset['marginBalance']}")
                s.append(f"錢包餘額: {asset['walletBalance']}")
                s.append(f"全部未實現損益: {asset['unrealizedProfit']}")
                s.append('\n')
                # update_time = render_epoch_time(asset['updateTime'])
                # print('updateTime: {}'.format(update_time))
            else:
                return
            
    s.append("部位:")
    for pos in res['positions']:
        symbol = pos['symbol']
        if symbol == 'BNBUSDT' or symbol == 'BTCUSDT':
            s.append(f"symbol: {symbol}")
            s.append(f"未實現損益: {pos['unrealizedProfit']}")
            s.append(f"持倉方向: {pos['positionSide']}")
            s.append(f"未實現損益: {pos['positionAmt']}")
            s.append(f"槓桿倍率: {pos['leverage']}")
            s.append('\n')
            # update_time = render_epoch_time(pos['updateTime'])
            # print('updateTime: {}'.format(update_time))
    return "\n".join(s)

# 帳戶餘額
def get_balance():
    url = 'https://fapi.binance.com/fapi/v2/balance'
    response = requests.get(url, headers=headers, params={
        'timestamp': timestamp,
        'signature': signature
    })
    print(response)
    print(json.dumps(response.json(), indent=4))

    for res in response.json():
        if res['asset'] == 'USDT':
            print(json.dumps(res, indent=4))


# binance internal withdraw (內部轉帳)
def withdraw(asset, amount):
    url = 'https://fapi.binance.com/fapi/v1/futures/transfer'
    response = requests.post(url, headers=headers, params={
        'timestamp': timestamp,  # 時間戳
        'signature': signature,  # 簽名
        'asset': asset,     # 轉帳幣種
        'amount': amount,   # 轉帳數量
        'type': 2           # 1: 現貨轉合約, 2: 合約轉現貨
    })
    print(response)
    print(json.dumps(response.json(), indent=4))

if __name__ == '__main__':
    s = get_account(margin=8000)
    if s != None:
        print(s)
        # line_notify_bot.send_line_notify(s)
        get_balance()
