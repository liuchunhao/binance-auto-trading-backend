#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Description: Binance websocket API
# 

from dotenv import load_dotenv
import json
import logging
import os

from binance.enums import FuturesType
from binance import ThreadedWebsocketManager
from binance import AsyncClient, BinanceSocketManager

from datetime import datetime

# client = AsyncClient()
# bsm = BinanceSocketManager(client)
# future = await bsm.futures_user_socket(callback=handle_futures_socket)


from common.constants import Payload            
from common.datetime import render_epoch_time, date_to_epoch, get_days_ago, get_day_count, epoch_to_date
from common.utils import left_align

import websocket.server.event_sender as event_sender

from service.binance.websocket.handler.ws_handler_futures_user_data import FuturesUserDataHandler

from websocket.server.ws_data_server import WebSocketServer

# subscribed_streams = set()

# def subscribe():
#     import queue
#     q = queue.Queue()
#     subscribed_streams.add(q)
    

def handle_socket_message(msg):
    json_str = json.dumps(msg, indent=4, sort_keys=True)
    logging.info(f"handle_socket_message: {json_str}")
    return msg


# markPriceUpdate per second
def handle_all_mark_price_socket(msg, symbol= ('BTCUSDT')):
    '''
     "data": [
            {
                "E": 1693640177001,         # event time
                "P": "25791.33141263",      # mark price: 標記價格
                "T": 1693641600000,         # next funding time
                "e": "markPriceUpdate",     # markPriceUpdate: 標記價格更新
                "i": "25789.55288380",      # index price: 指數價格
                "p": "25775.80000000",      # 標記價格的預估計算
                "r": "0.00001563",          # funding rate
                "s": "BTCUSD_PERP"          # PERP: 永續合約, 231229: 2023-12-29
            },
        ],
        "stream": "!markPrice@arr@1s"
    }
    '''
    json_str = json.dumps(msg, indent=4, sort_keys=True)
    logging.info(f"handle_all_mark_price_socket: {json_str}")

    data = [ data for data in msg['data'] if data['s'] in symbol ][0]
    result = f"""標記價格更新: 
    合約: {data['s']}
    標記價格: {data['p']}
    資金費率: {data['r']}
    """
    logging.info(f"handle_all_mark_price_socket: {result}")
    return data


def handle_multiplex_socket_book_ticker(msg):
    '''
    {
        "data": {
            "A": "3.66429000",          # best ask qty
            "B": "11.37066000",         # best bid qty
            "a": "25814.15000000",      # best ask price
            "b": "25814.14000000",      # best bid price
            "s": "BTCUSDT",             # symbol
            "u": 38618216721            # updateId
        },
        "stream": "btcusdt@bookTicker"
    }
    '''
    json_str = json.dumps(msg, indent=4, sort_keys=True)
    # stream = msg['stream'].replace('@bookTicker', '') 
    stream = msg['stream']
    msg['data']['stream'] = stream
    logging.info(f"handle_multiplex_socket(stream={stream}): {json_str}")
    return msg


def handle_trade_socket(msg):
    '''
    {
        "data": {
            "E": 1693635171421,
            "M": true,
            "T": 1693635171421,
            "a": 22217744714,
            "b": 22217746983,
            "e": "trade",           # event type
            "m": false,
            "p": "25830.00000000",
            "q": "0.00812000",
            "s": "BTCUSDT",
            "t": 3204267173
        },
        "stream": "btcusdt@trade"
    }
    '''


# then use its callback functions to bind to events
def handle_symbol_ticker_socket(msg):
    '''
    {
        "A": "5.05473000",              # ask price
        "B": "15.03446000",             # bid price
        "C": 1693582882123,             # close time
        "E": 1693582882123,             # event time
        "F": 3202744252,                # first trade id
        "L": 3203726935,                # last trade id
        "O": 1693496482123,             # open time
        "P": "-4.279",                  # price change percentage
        "Q": "0.07699000",              # quote volume
        "a": "25877.89000000",          # ask price
        "b": "25877.88000000",          # bid price
        "c": "25877.88000000",          # close price
        "e": "24hrTicker",              # event type
        "h": "27042.84000000",          # high price
        "l": "25566.53000000",          # low price
        "n": 982684,                    # total trades
        "o": "27034.69000000",          # open price
        "p": "-1156.81000000",          # price change
        "q": "1412876301.53061010",     # base volume
        "s": "BTCUSDT",                 # symbol
        "v": "53973.72884000",          # volume
        "w": "26177.11119643",          # weighted average price
        "x": "27034.68000000"           # previous day's close price
    }
    '''
    logging.info(f"handle_symbol_ticker_socket: {msg}")


# markPriceUpdate by symbol per second
def handle_symbol_mark_price_socket(msg):
    '''
    {
        "data": {
                "E": 1693640177001,         # event time
                "P": "25791.33141263",      # mark price: 標記價格
                "T": 1693641600000,         # next funding time
                "e": "markPriceUpdate",     # markPriceUpdate: 標記價格更新
                "i": "25789.55288380",      # index price: 指數價格
                "p": "25775.80000000",      # 標記價格的預估計算
                "r": "0.00001563",          # funding rate
                "s": "BTCUSD_PERP"          # PERP: 永續合約, 231229: 2023-12-29
        },
        "stream": "btcusdt@markPrice@1s"
    }
    '''
    json_str = json.dumps(msg, indent=4, sort_keys=True)
    logging.info(f"handle_symbol_mark_price_socket: {json_str}")

    data = msg['data']
    result = f"""
    [標記價格更新]
    合約: {data['s']}
    標記價格: {data['p']}
    資金費率: {data['r']}
    更新時間: {epoch_to_date(data['E'])}
    """

    result = left_align(result)

    # logging.info(f"handle_symbol_mark_price_socket: {result}")
    event_sender.publish(result)


# 現貨帳戶餘額異動 
def handle_user_socket(msg):
    '''
    # 訂閱: 現貨帳戶異動
    {
        "E": 1693576753148,   # event time
        "T": 1693576753147,   # transaction time
        "a": "USDT",          # asset
        "d": "5.00000000",    # delta
        "e": "balanceUpdate"  # event type
    }
    '''

    '''
    # 訂閱: 現貨帳戶餘額
    {
        "B": [                      # balance
            {
                "a": "USDT",        # asset
                "f": "5.00000000",  # free
                "l": "0.00000000"   # locked: 被鎖定或凍結的資產
            }
        ],
        "E": 1693576753148,                 # event time
        "e": "outboundAccountPosition",     # event type: outboundAccountPosition
        "u": 1693576753147                  # last account update time
    }
    '''

    json_str = json.dumps(msg, indent=4, sort_keys=True)
    logging.info(f"handle_user_socket: {json_str}")
    
    result = ''
    event_type = msg['e']
    if event_type == 'balanceUpdate':
        result = f"""
        [現貨帳戶異動]
        資產: {msg['a']}
        餘額異動: {msg['d']}
        異動時間: {epoch_to_date(msg['T'])}
        """
    elif event_type == 'outboundAccountPosition':
        result = f"""
        [現貨帳戶異動]
        資產: {msg['B'][0]['a']}
        餘額: {msg['B'][0]['f']}
        凍結: {msg['B'][0]['l']}
        異動時間: {epoch_to_date(msg['E'])}
        """
    else:
        result = f"現貨帳戶異動: unknown reason: {json_str}"    

    result = left_align(result)
    logging.info(f"handle_user_socket: {result}")

    # publish to websocket 
    event_sender.publish(result)
    

# 合約帳戶異動
def handle_futures_socket(msg):
    '''
    合約帳戶異動
    {
        "E": 1693578466218,
        "T": 1693578466217,
        "a": {
            "B": [
                {
                    "a": "USDT",
                    "bc": "1",
                    "cw": "54047.01942911",
                    "wb": "54047.01942911"
                }
            ],
            "P": [],
            "m": "DEPOSIT"
        },
        "e": "ACCOUNT_UPDATE"
    }
    '''
    
    '''
    委託單狀態
    {
        "E": 1693578610963,
        "T": 1693578610960,
        "e": "ORDER_TRADE_UPDATE",
        "o": {                               # order
            "L": "0",                        # last filled quantity
            "N": "USDT",                     # commission asset name
            "R": false,                      # reduceOnly
            "S": "SELL",                     # side: BUY, SELL
            "T": 1693578610960,              # trade time
            "V": "NONE",                # commission asset
            "X": "NEW",                 # 委託狀態: NEW, PARTIALLY_FILLED, FILLED, CANCELED, REJECTED, EXPIRED
            "a": "35",                  # last filled trade id
            "ap": "0",                  # average filled price
            "b": "0",                   # bids notional
            "c": "android_5XNuaDfCkopCM3vHd5p7",   # 客戶端設備ID     
            "cp": false,                # cross account: true, false
            "f": "GTC",                 # time in force: GTC, IOC, FOK
            "gtd": 0,                   # GMT 0
            "i": 186080772023,          # 訂單ID
            "l": "0",                   # last filled quantity
            "m": false,                 # is this trade the maker side?
            "n": "0",                   # commission        
            "o": "LIMIT",               # order type: LIMIT, MARKET, STOP, TAKE_PROFIT, STOP_MARKET, TAKE_PROFIT_MARKET, TRAILING_STOP_MARKET
            "ot": "LIMIT",              # original order type
            "p": "35000",               # 委託價格
            "pP": false,                # 是否觸發
            "pm": "NONE",               # position side: BOTH, LONG, SHORT
            "ps": "BOTH",               # position side: BOTH, LONG, SHORT
            "q": "0.001",               # 委託數量(BTC)
            "rp": "0",                  # realised profit of the trade
            "s": "BTCUSDT",             # symbol
            "si": 0,                    # stop price interval
            "sp": "0",                  # stop price
            "ss": 0,                    # stop price status
            "t": 0,                     # trade time    
            "wt": "CONTRACT_PRICE",         # working type: MARK_PRICE, CONTRACT_PRICE
            "x": "NEW",                     # order status: NEW, PARTIALLY_FILLED, FILLED, CANCELED, REJECTED, EXPIRED
            "z": "0"                        # cummulative filled quantity 
        }
    }
    
    '''
    json_str = json.dumps(msg, indent=4, sort_keys=True)
    logging.info(f"handle_futures_socket: {json_str}")
    return msg



class FuturesUserDataStream():

    def __init__(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s|%(levelname)-8s|%(message)s', datefmt='%Y%m%d %H:%M:%S')
        load_dotenv()
        self.api_key = os.getenv('API_KEY')
        self.api_secret = os.getenv('API_SECRET')
        self.__twm = ThreadedWebsocketManager(api_key=self.api_key, api_secret=self.api_secret)
        logging.info(f'FuturesUserDataStream|API_KEY={self.api_key} / API_SECRET={self.api_secret}')

        self.ws_data_server = WebSocketServer(host='0.0.0.0', port=28765)
        self.user_data_handler = FuturesUserDataHandler(callback=self.ws_data_server.broadcast)
        

    def publish(self, msg):
        logging.info(f"publish: {msg}")
        self.ws_data_server.broadcast(msg)
    

    def stop_all(self):
        self.__twm.stop()


    def stop(self, socket):
        self.__twm.stop_socket(socket)
    
        
    
    async def start(self):
        # 全部合約: 標記價格每秒更新一次(markPriceUpdate)
        # all_mark_price_socket = __twm.start_all_mark_price_socket(callback=handle_all_mark_price_socket, futures_type=FuturesType.USD_M) 
        
        # symbol = 'BTCUSDT'
        # 單一合約: 標記價格每秒更新一次(markPriceUpdate)
        # symbol_mark_price_socket = __twm.start_symbol_mark_price_socket(callback=handle_symbol_mark_price_socket, symbol=symbol, futures_type=FuturesType.USD_M) # markPrice

        # 現貨: 帳戶餘額異動
        #  user_socker = __twm.start_user_socket(callback=handle_user_socket)                               # Spot User Streams
        
        # 合約交易狀態異動
        # futures_socket = __twm.start_futures_socket(callback=handle_socket_message)        # Futures Streams

        # 合約最新成交最佳價格
        # symbol_ticker_socket = __twm.start_symbol_ticker_socket(callback=handle_symbol_ticker_socket, symbol=symbol) # bookTicker

        # or a multiplex socket can be started like this:  
        # streams = ['bnbusdt@ticker', 'btcusdt@ticker']
        # streams = ['bnbusdt@miniTicker', 'btcusdt@miniTicker']
        # streams = ['bnbusdt@bookTicker', 'btcusdt@bookTicker']
        # streams = ['btcusdt@bookTicker']
        # streams = ['btcusdt@markPrice@1s']
        # streams = ['btcusdt@trade']

        # __twm.start_multiplex_socket(callback=handle_socket_message, streams=streams) 
        # __twm.start_coin_futures_socket(callback=handle_socket_message)                                    # bookTicker
        # __twm.start_kline_socket(callback=handle_socket_message, symbol=symbol)                            # Kline/Candlestick Streams
        # __twm.start_depth_socket(callback=handle_socket_message, symbol=symbol)                            # Order Book Streams
        # __twm.start_trade_socket(callback=handle_socket_message, symbol=symbol)                            # Trade Streams
        # __twm.start_symbol_ticker_futures_socket(callback=handle_socket_message, symbol=symbol)            # bookTicker
        # __twm.start_individual_symbol_ticker_futures_socket(callback=handle_socket_message, symbol=symbol) # bookTicker

        # sleep for 5 seconds
        # import time
        # time.sleep(5)

        # start up websocket producer
        # event_sender.start()

        # logging.info(f"start up websocket producer")
        # ws_data_server.start()

        # Futures User Data Streams
        try: 

            # self.__twm.start() # start is required to initialise its internal loop
            # futures_user_socket = self.__twm.start_futures_user_socket(callback=user_data_handler.handle)     
            # logging.info(f"wait for websocket to start receiving messages")  
            # self.__twm.join()   # wait for websocket to start receiving messages

            self.client = await AsyncClient.create(api_key=self.api_key, api_secret=self.api_secret)
            self.bsm = BinanceSocketManager(self.client)

            async with self.bsm.futures_user_socket() as stream:
                while True:
                    res = await stream.recv()
                    self.user_data_handler.handle(res)
            await client.close_connection()

        except Exception as e:
            logging.error(e)   
            logging.info(f"stop all streams")


    async def main(self):
        import asyncio
        try:
            tasks = [
                asyncio.create_task(self.start()),
                asyncio.create_task(self.ws_data_server.main()),
            ]
            done, pending = await asyncio.wait(tasks)
        except KeyboardInterrupt:
            logging.info("Websocket server stopped")
        finally:
            pass
