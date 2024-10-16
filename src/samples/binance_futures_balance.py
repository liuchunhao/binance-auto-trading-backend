from binance.client import Client
from binance.streams import ThreadedWebsocketManager

import config

# 输入您的 Binance API 密钥
api_key = config.KEY
api_secret = config.SECRET

# 创建客户端实例
client = Client(api_key, api_secret)

# 订阅实时余额变化通知
def process_message(msg):
    print("Real-time account balance change:", msg)

bm = ThreadedWebsocketManager(client)
bm.start()
futures_symbol = "BTCUSDT"
stream = futures_symbol.lower() + "@balance"
conn_key = bm.start_futures_user_socket(process_message, stream=stream)
bm.join()
