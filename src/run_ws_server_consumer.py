# Binance Websocket API

# websocket: consumer 
from websocket.server import cmd_receiver 
from websocket.server.ws_data_server import WebSocketServer

if __name__ == '__main__':
    # cmd_receiver.start()

    WebSocketServer().start()
    