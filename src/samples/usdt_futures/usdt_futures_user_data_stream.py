import hashlib
import hmac
import time
import requests
import websocket
import json

API_KEY = '1XHbm0oQXt0ocT4NlSEsejfyLhnErejQXqcOxGdVTAE1I0XyZNgkdXFhF4ojmksw'      # Binance API production
SECRET_KEY = b'O7F7iXmMKFhXLwwIPfhKBMxo9yOsD5GjmgafzYEkMoDvK4C13PbqF7ei2qCmGT1c'  # bytes

URL = 'https://fapi.binance.com/fapi/v1/listenKey'
WS_URL = 'wss://fstream.binance.com/ws'

headers = {
    'X-MBX-APIKEY': API_KEY
}

listen_key = ''

def get_listen_key():
    response = requests.post(URL, headers=headers)
    if response.status_code == 200:
        listen_key = response.json()['listenKey']
        print('User data stream started with listenKey: {}'.format(listen_key))
    else:
        print('Failed to start user data stream')

def on_message(ws, message):
    print('on_message:')
    msg = json.loads(message)
    render_resp(msg)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    print('User data stream opened:')

    # __suscribe(ws)
    # __request(ws, listen_key)
    __account_update(ws, API_KEY, SECRET_KEY, listen_key)


# 1. 訂閱
def __suscribe(ws):
    request = json.dumps({ "method": "SUBSCRIBE",
                           "params":[ 
                                      # 同一價格,同一方向,同時間(100ms)的trade會被聚合成一條
                                      "btcusdt@aggTrade",      

                                      # 5檔:
                                      # "btcusdt@depth5@500ms",  
                                      # "bnbusdt@depth5@500ms",

                                      # 最新 MarkPrice:
                                      "btcusdt@markPrice@1s",  
                                      # "bnbusdt@markPrice@3s",  

                                     ],
                           "id": 1 })
    ws.send(request)

# 2. 請求
def __request(ws, listen_key):
    request = json.dumps({ "method": "REQUEST",
                           "params":[ 
                                        "{}@account".format(listen_key),
                                        "{}@balance".format(listen_key),
                                        "{}@position".format(listen_key),
                                     ],
                           "id": 2 })
    ws.send(request)

def __account_update(ws, api_key, secret_key, listen_key):
    ts = int(time.time() * 1000)
    signature = hmac.new(SECRET_KEY, f'timestamp={ts}'.encode('utf-8'), hashlib.sha256).hexdigest()
    payload = {
        'apiKey': API_KEY,
        'timestamp': ts,
        'signature': signature
    }
    ws.send(json.dumps({
        'method': 'SUBSCRIBE',
        'params': [ 
            f'{API_KEY}@balance',
            f'{listen_key}@account',
            f'{listen_key}@balance',
        ],
        'id': 1
    }))

    time.sleep(1)
    ws.send(json.dumps({
        'method': 'START_USER_DATA_STREAM',
        'params': payload,
        'id': 2
    }))

def render_epoch_time(epoch_time):
    import datetime
    epoch_time = epoch_time // 1000  # convert miliseconds to seconds
    human_time = datetime.datetime.fromtimestamp(epoch_time).strftime('%Y-%m-%d %H:%M:%S')
    return human_time


def on_resp_default(msg):
    print(msg)

# 五檔更新事件
def on_resp_depth(msg):
    '''
    e: 事件類型，表示這是一個深度更新事件 (depthUpdate)
    E: 事件時間，表示這個事件發生的時間 (Epoch 時間，單位為毫秒)
    T: 成交時間，表示最後一筆交易的時間 (Epoch 時間，單位為毫秒)
    s: 交易對，表示這個深度更新是哪一個交易對的深度更新 (e.g. BTCUSDT)
    U: 第一筆更新 ID，表示從這個更新 ID 後的所有深度更新，都是本次更新所帶來的變化，必須重新計算深度
    u: 最後一筆更新 ID，表示這個深度更新的最後一筆更新的 ID
    pu: 上一個更新 ID，表示這個深度更新的前一筆更新的 ID
    b: bids，表示買單深度，從高到低排序，每個陣列裡有兩個元素，分別是價格和數量
    a: asks，表示賣單深度，從低到高排序，每個陣列裡有兩個元素，分別是價格和數量
    '''
    event_time = msg['E']
    trade_time = msg['T']
    symbol = msg['s']
    bids = msg['b']
    asks = msg['a']

# Mark Price 的更新事件
def on_resp_mark_price(msg):
    '''
    "e": "markPriceUpdate" 表示這是一個 Mark Price 的更新事件。
    "E": 1676807160000 表示該事件發生的時間戳 (epoch time)，單位為毫秒 (ms)。
    "s": "BTCUSDT" 表示該事件涉及的交易對。
    "p": "24660.37123526" 表示最新的 Mark Price。
    "P": "24666.89940380" 表示預估下一個買方合約的 Mark Price。
    "i": "24661.08862651" 表示預估下一個賣方合約的 Mark Price。
    "r": "0.00010000" 表示資金費用 (funding rate)，即持有合約的成本。
    "T": 1676822400000 表示下一個資金費用的時間戳 (epoch time)，單位為毫秒 (ms)。
    '''
    event_time = msg['E']

    trade_time = msg['T']
    symbol = msg['s']
    bids = msg['b']
    asks = msg['a']

# 聚合交易
def on_resp_agg_trade(msg):
    '''
    "e": "aggTrade"，表示事件的類型為"aggTrade"，即聚合交易。
    "E": 1676807159373，表示該事件的時間戳，單位為毫秒。
    "a": 1606458080，表示該交易的ID。
    "s": "BTCUSDT"，表示交易對為BTC/USDT。
    "p": "24659.80"，表示成交價格。
    "q": "0.022"，表示成交數量。
    "f": 3308682632，表示該成交的首個交易ID。
    "l": 3308682632，表示該成交的最後一個交易ID。
    "T": 1676807159282，表示成交時間的時間戳，單位為毫秒。
    "m": true，表示成交方向為買入（maker），false為賣出（taker）。
    '''
    event_time = msg['E']
    trade_time = msg['T']
    symbol = msg['s']
    bids = msg['b']
    asks = msg['a']

EVENT_TYPE = {
    'MARGIN_CALL': on_resp_depth,
    'ACCOUNT_UPDATE': on_resp_agg_trade,
    'ORDER_TRADE_UPDATE': on_resp_mark_price,
} 

def render_resp(msg):
    '''
    e: 事件類型，表示這是一個深度更新事件 (depthUpdate)
    E: 事件時間，表示這個事件發生的時間 (Epoch 時間，單位為毫秒)
    T: 成交時間，表示最後一筆交易的時間 (Epoch 時間，單位為毫秒)
    s: 交易對，表示這個深度更新是哪一個交易對的深度更新 (e.g. BTCUSDT)
    U: 第一筆更新 ID，表示從這個更新 ID 後的所有深度更新，都是本次更新所帶來的變化，必須重新計算深度
    u: 最後一筆更新 ID，表示這個深度更新的最後一筆更新的 ID
    pu: 上一個更新 ID，表示這個深度更新的前一筆更新的 ID
    b: bids，表示買單深度，從高到低排序，每個陣列裡有兩個元素，分別是價格和數量
    a: asks，表示賣單深度，從低到高排序，每個陣列裡有兩個元素，分別是價格和數量
    '''
    formatted_data = json.dumps(msg, indent=4)
    print(formatted_data)

    if 'e' in msg:
        event_type = msg['e']
        EVENT_TYPE.get(event_type, on_resp_default)(msg)
    else:
        on_resp_default(msg)


# 關閉User Data Stream
def close():
    response = requests.delete(URL, headers=headers)
    if response.status_code == 200:
        print('User data stream stopped')
    else:
        print('Failed to stop user data stream')


if __name__ == "__main__":
    listen_key = get_listen_key()

    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("{}/{}".format(WS_URL, listen_key),
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()
