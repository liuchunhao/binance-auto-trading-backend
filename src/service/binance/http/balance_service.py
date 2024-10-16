#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Description: Binance websocket API

import os
import logging
import datetime
import json
import yaml

from binance import ThreadedWebsocketManager
from binance.client import Client
from dotenv import load_dotenv

from common.constants import Payload            # from src.common.constants import Payload
from common.datetime import render_epoch_time, date_to_epoch, get_days_ago, get_day_count, epoch_to_date
from service.linebot.notification import send_line_notify
from common.utils import beautify_json, format_float

logging.basicConfig(level=logging.INFO, format='%(asctime)s|%(levelname)-8s|%(message)s', datefmt='%Y%m%d %H:%M:%S')
load_dotenv()

api_key = os.getenv('API_KEY')
api_secret = os.getenv('API_SECRET')

logging.info(f'API_KEY={api_key}')
logging.info(f'API_SECRET={api_secret}')

symbol = 'BNBUSDT'

from service.binance.http.client import RevisedBinanceClient
client = RevisedBinanceClient(api_key=api_key, api_secret=api_secret)

# 設定檔
logging.info(f'search_path: {os.getcwd()}')
with open('src/config.yml', 'r') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
    logging.info(f'config: {config}')

# 1. spot balance (現貨帳戶餘額)
def get_spot_balance(asset='USDT'):
    result = client.get_asset_balance(asset=asset)
    logging.info(f'get_spot_balance: {json.dumps(result, indent=4, sort_keys=True)}')
    return result

# 2. account balance (帳戶餘額)
def get_account_balance():
    result = client.get_account()
    balances = result['balances']
    # logging.info(f'balances: {json.dumps(balances, indent=4, sort_keys=True)}')

    resp = ''
    for balance in balances:
        asset = balance['asset']
        free = float(balance['free'])
        locked = float(balance['locked'])
        if free > 0 or locked > 0:
            resp += f'''
            資產: {asset}
            可用: {free}
            鎖定: {locked}
            '''
    lines = resp.splitlines()
    stripped = [line.strip() for line in lines]
    resp = '\n'.join(stripped)
    logging.info(f'{resp}')
    return result, resp

# 3. futures balance (合約帳戶餘額)
def get_futures_balance()->dict:
    return client.futures_account_balance(version='v2')

# 4. funding balance (永續合約帳戶餘額)
def get_funding_asset()->dict:
    return client.futures_position_information()

def futures_ping()->dict:
    return client.futures_ping()
