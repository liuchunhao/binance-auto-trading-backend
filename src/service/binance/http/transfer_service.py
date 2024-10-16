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
client = Client(api_key, api_secret)

# 設定檔
logging.info(f'search_path: {os.getcwd()}')
with open('src/config.yml', 'r') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
    logging.info(f'config: {config}')


# 0. transfer (general)
def transfer(amount, type, asset='USDT'):
    result = client.futures_account_transfer(
        asset=asset,
        amount=amount,
        timestamp=date_to_epoch(datetime.datetime.now()),
        type=type       # 1: transfer from spot account to USDT-Ⓜ futures account. 
                        # 2: transfer from USDT-Ⓜ futures account to spot account.
                        # 3: transfer from spot account to COIN-Ⓜ futures account.
                        # 4: transfer from COIN-Ⓜ futures account to spot account.
    )
    logging.info(f'futures_transfer_to_spot: {json.dumps(result, indent=4, sort_keys=True)}')
    return result

# 1. futures to sport transfer (轉帳: 合約->現貨)
def futures_transfer_to_spot(amount, asset='USDT'):
    result = client.futures_account_transfer(
        asset=asset,
        amount=amount,
        timestamp=date_to_epoch(datetime.datetime.now()),
        type=2          # 1: transfer from spot account to USDT-Ⓜ futures account. 
                        # 2: transfer from USDT-Ⓜ futures account to spot account.
                        # 3: transfer from spot account to COIN-Ⓜ futures account.
                        # 4: transfer from COIN-Ⓜ futures account to spot account.
    )
    logging.info(f'futures_transfer_to_spot: {json.dumps(result, indent=4, sort_keys=True)}')
    return result

# 2. spot to futures transfer (轉帳: 現貨->合約)
def spot_transfer_to_futures(amount, asset='USDT'):
    result = client.futures_account_transfer(
        asset=asset,
        amount=amount,
        timestamp=date_to_epoch(datetime.datetime.now()),
        type=1          # 1: transfer from spot account to USDT-Ⓜ futures account. 
                        # 2: transfer from USDT-Ⓜ futures account to spot account.
                        # 3: transfer from spot account to COIN-Ⓜ futures account.
                        # 4: transfer from COIN-Ⓜ futures account to spot account.
    )
    logging.info(f'spot_transfer_to_futures: {json.dumps(result, indent=4, sort_keys=True)}')
    # return result['tranId']
    return result


# 3. transfer history list (轉帳歷史紀錄查詢)
def get_transfer_history_list(days=7, asset='USDT'):
    transfer_history = client.transfer_history(
        startTime=date_to_epoch(get_days_ago(days=days)),
        timestamp=date_to_epoch(datetime.datetime.now()),
        asset=asset
    )
    logging.info(f'''get_transfer_history_list: {json.dumps(transfer_history, indent=2, sort_keys=True)}
    type: 
        1: transfer from spot account to USDT-Ⓜ futures account. 
        2: transfer from USDT-Ⓜ futures account to spot account. 
        3: transfer from spot account to COIN-Ⓜ futures account. 
        4: transfer from COIN-Ⓜ futures account to spot account.''')
    return transfer_history
