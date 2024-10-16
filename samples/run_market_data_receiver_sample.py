import websocket
import json

# 訂閱深度資訊
def on_open(ws):
    msg = {
        "method": "SUBSCRIBE",
        "params":
        [
            # "btcusd_perp@ticker"
            "btcusd@ticker"
        ],
        "id": 1
    }
    res = ws.send(json.dumps(msg))
    print('on_open:'.format(res))

# 接收資料
def on_message(ws, message):
    print(json.loads(message))
    print(json.loads(message)['data'])

# 連接 WebSocket API
# ws = websocket.WebSocketApp("wss://fstream.binance.com/ws",
#                            on_open=on_open,
#                            on_message=on_message)

# trading pair
ws = websocket.WebSocketApp("wss://fstream.binance.com/stream?streams=btcusdt@ticker", on_message=on_message)    
# BTC/USDT trade data
ws = websocket.WebSocketApp("wss://fstream.binance.com/stream?streams=btcusdt@aggTrade", on_message=on_message)  
# order book depth
ws = websocket.WebSocketApp("wss://fstream.binance.com/stream?streams=btcusdt@depth", on_message=on_message)     


if __name__ == '__main__':
    # 開始執行
    ws.run_forever()

