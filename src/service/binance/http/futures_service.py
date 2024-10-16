#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Description: Binance websocket API

import os
import logging
import datetime
import json
import yaml
from dotenv import load_dotenv

from binance import ThreadedWebsocketManager
from binance.client import Client
from service.binance.http.client import RevisedBinanceClient

from common.constants import Payload            # from src.common.constants import Payload
from common.datetime import render_epoch_time, date_to_epoch, get_days_ago, get_day_count, epoch_to_date
from common.utils import beautify_json, format_float

from service.linebot.notification import send_line_notify

from model.r import R

logging.basicConfig(level=logging.INFO, format='%(asctime)s|%(levelname)-8s|%(message)s', datefmt='%Y%m%d %H:%M:%S')

load_dotenv()

api_key = os.getenv('API_KEY')
api_secret = os.getenv('API_SECRET')

logging.info(f'API_KEY={api_key}')
logging.info(f'API_SECRET={api_secret}')

symbol = 'BNBUSDT'
client = Client(api_key, api_secret)
revised_client = RevisedBinanceClient(api_key=api_key, api_secret=api_secret)

logging.info(f'search_path: {os.getcwd()}')

with open('src/config.yml', 'r') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
    logging.info(f'config: {config}')


# NEW ORDER
def futures_create_order(symbol, quantity, side, type='LIMIT', price=0, timeInForce='GTC', poisitionSdie='BOTH'):
    result = client.futures_create_order(
        timestamp=date_to_epoch(datetime.datetime.now()),
        symbol=symbol,              # BTCUSDT, BNBUSDT
        quantity=quantity,
        price=price,            
        side=side,                  # BUY, SELL
        type=type,                  
        positionSide=poisitionSdie, 
        recvWindow=10000,
        timeInForce=timeInForce,    # GTC, IOC, FOK
    )
    logging.info(f'futures_create_order: {json.dumps(result, indent=4, sort_keys=True)}')
    return result


# LIMIT ORDER
def limit_order(symbol, side, quantity, price, reduceOnly=False):
    result = client.futures_create_order(
        timestamp=date_to_epoch(datetime.datetime.now()),
        positionSide='BOTH',    
        recvWindow=10000,
        timeInForce='GTC',      # GTC, IOC, FOK, GTX
        type='LIMIT',           
        symbol=symbol,          
        side=side,              
        quantity=quantity,
        price=price,            
        reduceOnly=reduceOnly,  # true: 只減倉, false: 可增減倉
    )
    logging.info(f'limit_order: {json.dumps(result, indent=4, sort_keys=True)}')
    return result


# MARKET ORDER
def market_order(symbol, side, quantity):
    result = client.futures_create_order(
        timestamp=date_to_epoch(datetime.datetime.now()),
        positionSide='BOTH',    
        recvWindow=10000,
        # timeInForce='GTC',      Not allowed in MARKET order
        type='MARKET',          
        symbol=symbol,         
        side=side,              
        quantity=quantity,
    )
    logging.info(f'market_order: {json.dumps(result, indent=4, sort_keys=True)}')
    return result


# STOP_MARKET, TAKE_PROFIT_MARKET
def stop_market(symbol, side, stopPrice, quantity, workingType='CONTRACT_PRICE', timeInForce='GTC', poisitionSdie='BOTH'):
    result = client.futures_create_order(
        timestamp=date_to_epoch(datetime.datetime.now()),
        recvWindow=10000,
        # closePosition=True,       # Not allowed used with 'quantity' 
        timeInForce=timeInForce,    # GTC, IOC, FOK
        workingType=workingType,
        positionSide=poisitionSdie, 
        type='STOP_MARKET',         # STOP_MARKET, TAKE_PROFIT_MARKET
        symbol=symbol,              
        side=side,                  
        stopPrice=stopPrice,
        quantity=quantity,
    )
    logging.info(f'stop_market: {json.dumps(result, indent=4, sort_keys=True)}')
    return result


# STOP_LIMIT, TAKE_PROFIT_LIMIT
def stop_limit(symbol, side, stopPrice, price, quantity, workingType='CONTRACT_PRICE', timeInForce='GTC'):
    logging.info(f'stop_limit: {locals()}')
    result = client.futures_create_order(
        timestamp=date_to_epoch(datetime.datetime.now()),
        recvWindow=10000,
        timeInForce=timeInForce,    
        workingType=workingType,
        positionSide='BOTH',        # LONG, SHORT: Bi-directional Position;  BOTH: One-way Positions(default) 
        reduceOnly=True,            # 不能在雙向持倉模式下使用 reduceOnly
        type='STOP',                # STOP
        symbol=symbol,              
        side=side,                  
        quantity=quantity,
        stopPrice=stopPrice,
        price=price,            
    )
    logging.info(f'stop_limit: {json.dumps(result, indent=4, sort_keys=True)}')
    return result


# CANCEL ORDER
def futures_cancel_order(symbol, orderId):
    # DELETE /fapi/v1/order (HMAC SHA256)
    result = client.futures_cancel_order(
        timestamp=date_to_epoch(datetime.datetime.now()),
        recvWindow=10000,
        symbol=symbol,
        orderId=orderId,          # 訂單ID
        # origClientOrderId='',   # 用戶自定義的訂單ID, 用於取消訂自定義單
    )
    logging.info(f'futures_cancel_order: {json.dumps(result, indent=4, sort_keys=True)}')
    return result


# CANCEL ALL OPEN ORDERS
def futures_cancel_all_open_orders(symbol):
    # DELETE /fapi/v1/order (HMAC SHA256)
    result = client.futures_cancel_all_open_orders(
        timestamp=date_to_epoch(datetime.datetime.now()),
        symbol=symbol,
    )
    logging.info(f'futures_cancel_all_open_orders: {json.dumps(result, indent=4, sort_keys=True)}')
    return result


# PUT / MODIFY ORDER
def modify_order(orderId, symbol, side, quantity, price):
    params = {
        'orderId': orderId,
        'symbol': symbol,
        'side': side,
        'quantity': quantity,
        'price': price,
        'timestamp': date_to_epoch(datetime.datetime.now()),
        'recvWindow': 10000
    }
    result = client._request_futures_api("put", "order", True, data=params);
    logging.info(f'modify order: {json.dumps(result, indent=4, sort_keys=True)}')
    return result


# GET / Account Trades List 
def futures_account_trades(symbol, limit: int=50):
    result = client.futures_account_trades(
        timestamp=date_to_epoch(datetime.datetime.now()),
        recvWindow=10000,
        symbol=symbol,          # Default 500; max 1000.
        limit=limit
    )
    logging.info(f'futures_account_trades: {json.dumps(result, indent=4, sort_keys=True)}')
    return result


# get open orders by symbol (委託查詢 - 合約)
def futures_get_open_orders(symbol):
    result = client.futures_get_open_orders(
        timestamp=date_to_epoch(datetime.datetime.now()),
        recvWindow=10000,
        symbol=symbol,
    )
    logging.info(f'futures_get_open_orders: {json.dumps(result, indent=4, sort_keys=True)}')
    return result


# get all open orders (委託查詢 - 全部)
def futures_get_all_open_orders():
    result = client.futures_get_open_orders(
        timestamp=date_to_epoch(datetime.datetime.now()),
        recvWindow=10000
    )
    logging.info(f'futures_get_all_open_orders: {json.dumps(result, indent=4, sort_keys=True)}')
    return result


# futures get order by orderId (合約委託查詢 - 單筆)
def futures_get_order_by_orderId(symbol, orderId):
    result = client.futures_get_order(
        timestamp=date_to_epoch(datetime.datetime.now()),
        recvWindow=10000,
        symbol=symbol,
        orderId=orderId,
    )
    logging.info(f'futures_get_order_by_orderId: {json.dumps(result, indent=4, sort_keys=True)}')
    return result


# positions 
def futures_position():
    result = revised_client.futures_position_information() # fapi/v2
    return result


# history / my trades
def my_trades(symbol, limit: int=10):
    # https://binance-docs.github.io/apidocs/spot/en/#account-trade-list-user_data
    result = client.get_my_trades(
        symbol=symbol,
        # orderId=None,
        # startTime=None,
        # endTime=None,
        # fromId=None,
        limit=limit
    ) 
    return result


#  account 
def account ():
    result = revised_client.get_account()
    return result
