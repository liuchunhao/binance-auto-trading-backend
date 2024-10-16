#!/usr/bin/env python

# import os
# import logging
# import datetime
# import json
# import yaml

# from binance import ThreadedWebsocketManager
# from binance.client import Client
# from dotenv import load_dotenv

# from common.constants import Payload            # from src.common.constants import Payload
# from common.datetime import render_epoch_time, date_to_epoch, get_days_ago, get_day_count, epoch_to_date
# from service.linebot.notification import send_line_notify
# from common.utils import beautify_json, format_float

# logging.basicConfig(level=logging.INFO, format='%(asctime)s|%(levelname)-8s|%(message)s', datefmt='%Y%m%d %H:%M:%S')
# load_dotenv()

# api_key = os.getenv('API_KEY')
# api_secret = os.getenv('API_SECRET')

# logging.info(f'API_KEY={api_key}')
# logging.info(f'API_SECRET={api_secret}')

# symbol = 'BNBUSDT'
# client = Client(api_key, api_secret)

# # 設定檔
# logging.info(f'search_path: {os.getcwd()}')
# with open('src/config.yml', 'r') as f:
#     config = yaml.load(f, Loader=yaml.FullLoader)
#     logging.info(f'config: {config}')

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


# 1. withdraw (匯出)到指定錢包地址 
def withdraw(coin='USDT', network: str='TRX', address: str='TJVgcdikVX9uavZmhPuTGBahyPxJ5bcYop', walletType: int=0, amount: float=0.0)->dict:
    # network:
    # TRX: TRC20 , ETH: ERC20

    # whitelisted address:
    # TRX: TJVgcdikVX9uavZmhPuTGBahyPxJ5bcYop
    # ETH: 0x9d0b7b1d98a20001387f0de8e8ddc91b0126822a

    logging.info(f'withdraw: network={network}, address={address}, walletType={walletType}, amount={amount}')
    result = client.withdraw (
        coin=coin,
        address=address,
        amount=amount,
        network=network,
        walletType=walletType        # 0: spot wallet,    1: funding wallet
    )
    logging.info(f'withdraw result: {json.dumps(result, indent=4, sort_keys=True)}')
    return result

# 2. withdraw history (出金歷史記錄)
def get_withdraw_history(offset=0, limit=1):
    logging.info(f'get_withdraw_history: offset={offset}, limit={limit}')
    withdraw_history = client.get_withdraw_history(
        offset=offset,
        limit=limit
    )
    # 0:Email Sent, 1:Cancelled, 2:Awaiting Approval, 3:Rejected, 4:Processing, 5:Failure, 6:Completed
    logging.info(f'withdraw_history: {json.dumps(withdraw_history, indent=4, sort_keys=True)}')    
    return withdraw_history

# 3. withdraw status code (出金狀態碼)
def get_withdraw_status_code()->dict:
    # 0:Email Sent,1:Cancelled 2:Awaiting Approval 3:Rejected 4:Processing 5:Failure 6:Completed
    # return '''{ 0:Email Sent, 1:Cancelled, 2:Awaiting Approval, 3:Rejected, 4:Processing, 5:Failure, 6:Completed }'''
    return {
        0: 'Email Sent',
        1: 'Cancelled',
        2: 'Awaiting Approval',
        3: 'Rejected',
        4: 'Processing',
        5: 'Failure',
        6: 'Completed'
    }
