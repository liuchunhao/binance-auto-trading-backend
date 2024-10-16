# Binance Websocket API
import logging

from websocket.server.ws_data_server import WebSocketServer

if __name__ == '__main__':
    server = WebSocketServer(host='0.0.0.0', port=28765)
    logging.info(f"Websocket server started at ws://{server.host}:{server.port}")
    server.start()
