import time
import logging
from binance.lib.utils import config_logging
from binance.spot import Spot as Client
from binance.websocket.spot.websocket_client import SpotWebsocketClient
from src.config import key

config_logging(logging, logging.DEBUG)


def message_handler(message):
    print(message)


client = Client(key=key)
# client = Client(key=key, base_url='https://testnet.binance.vision/api')
response = client.new_listen_key()
print('session:{}'.format(client.session.headers))

logging.info("Receving listen key : {}".format(response["listenKey"]))

ws_client = SpotWebsocketClient()
# ws_client = SpotWebsocketClient(stream_url="wss://testnet.binance.vision")
ws_client.start()

ws_client.user_data(
    listen_key=response["listenKey"],
    id=1,
    callback=message_handler,
)

# Combine selected streams
ws_client.instant_subscribe(
    stream=['bnbusdt@bookTicker', 'ethusdt@bookTicker'],
    callback=message_handler,
)

time.sleep(10)

#ws_client.stop()
#logging.debug("closing ws connection")
