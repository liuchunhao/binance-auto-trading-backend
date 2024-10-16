#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Description: Binance websocket API

import os
import logging
import json
import yaml

from binance.client import Client
from dotenv import load_dotenv

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

# 1. deposit addres (入金錢包地址)
def get_deposit_address(network='TRX')->dict:
    # TRX, TRC20 
    # ETH, ERC20
    deposit_address = client.get_deposit_address(coin='USDT', network=network)
    logging.info(f'deposit_address(network: {network}): {json.dumps(deposit_address, indent=4, sort_keys=True)}')
    return deposit_address

# 2. deposit history (入金歷史記錄)
def get_deposit_history(offset=0, limit=1)->dict:
    deposit_history = client.get_deposit_history(offset=0, limit=1)
    # 0:pending, 1:success
    logging.info(f'deposit_history: {json.dumps(deposit_history, indent=4, sort_keys=True)}')
    return deposit_history
