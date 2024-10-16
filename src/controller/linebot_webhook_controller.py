import re
import os
import logging
from dotenv import load_dotenv
from typing import Optional

from flask import request, Blueprint, abort
from flask_caching import Cache

from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (MessageEvent, TextMessage, TextSendMessage,)

from service.binance.user_data import parse_mt5_account_status, get_futures_account_status
from common.database import insert_mt5_balance

from service.binance import user_data
from common.database import insert_mt5_balance
from common.utils import *

from server.handler import help
from server.handler import order
from server.handler import transfer
from server.handler import deposit
from server.handler import withdraw
from server.handler import balance

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s|%(levelname)-8s|%(message)s', datefmt='%Y%m%d %H:%M:%S')

# 設定
load_dotenv()
access_token = os.getenv('CHANNEL_ACCESS_TOKEN')
secret = os.getenv('CHANNEL_SECRET')

# LINE Webhook
line_bot_api = LineBotApi(access_token)
webhook_handler = WebhookHandler(secret)

bp = Blueprint('linebot_webhook_controller', __name__)

# 創建 Flask Cache 實例
cache = Cache(config={'CACHE_TYPE': 'redis'})

# LINE Webhook
@bp.route("/callback", methods=['POST'])
def callback():
    '''
        Headers:
        Host: c3ad-61-222-207-211.ngrok-free.app
        User-Agent: LineBotWebhook/2.0
        Content-Length: 63
        Content-Type: application/json; charset=utf-8
        X-Forwarded-For: 147.92.150.197
        X-Forwarded-Proto: https
        X-Line-Signature: RiVbPpl/FGWVv3xZHCC8PoMZ3rqfBkq/0OI6Azpq5XM=
        Accept-Encoding: gzip
    '''

    try:
        logging.info(f"headers:${request.headers}")
        # get X-Line-Signature header value
        signature = request.headers['X-Line-Signature']

        # get request body as text
        '''
        {"destination":"U6b3c56b87b58546a67a552e6ae316eaa","events":[]}
        '''
        body = request.get_data(as_text=True)
        logging.info("signature: " + signature)
        logging.info("request_body: " + body)

        # handle webhook body
        webhook_handler.handle(body, signature)
    except Exception as e:
        logging.exception('Got exception on main handler')
        abort(400)
    return 'OK'


# 處理所有來自Line群組的訊息
@webhook_handler.add(MessageEvent, message=TextMessage)
def handle(event):
    command = parse_command(event.message.text)             # 解析命令参数
    if command:
        reply_text = dispatch(command)                      # 分派處理任務
        # 回覆LINE訊息
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_text)
        )
    else:
        # 無效命令不處理不回應(群組對話太多)
        reply_text = f'Unknown command: [{event.message.text}]' 


# 解析所有來自Line群組的訊息
def parse_command(text):
    logging.info(f'parse_command: [{text}]')
    pattern = r'!{1}\s*(.*)'
    text = text.strip()
    match = re.match(pattern, text, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    else:
        # 來自MT5的訊息
        # you CANNOT receive message from other LINE chatbot !

        pattern = '【MT5】((?:.|\n)*)回報((?:.|\n)*)'
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            margin, balance = parse_mt5_account_status(match.string)
            insert_mt5_balance(margin=margin, balance=balance)
            return 'position-mt5'
        else:
            return None

def dispatch(command):
    try: 
        last_command = cache.get('last_command')
        if command is None:
            return 'Unknown command'

        logging.info(f'last command: [{last_command}]')
        logging.info(f'recv command: [{command}]')

        copied_command = last_command
        if command == '!':
            command = last_command

        if command is None:
            reply_text = 'Unknown command.'
        else:
            if command == 'ping':
                reply_text = 'pong'
            elif command == 'help':
                reply_text = left_align(help.get_help_message())
            elif command == 'fee':
                reply_text = user_data.get_total_latest_funding_fee()
            elif command == 'position':
                total_margin_balance, margin, reply_text = user_data.get_futures_account_status()
            elif command == 'position-mt5':
                total_margin_balance, margin, reply_text = user_data.get_futures_account_status()
                reply_text = f'收到MT5的部位回報:\n{reply_text}'
            elif command.startswith('balance'):
                reply_text = balance._balance(command)
            elif command.startswith('order'):
                # 委託: 下單、刪單、平倉、查詢
                reply_text = order._create_order(command)
            elif command.startswith('withdraw'):
                # 提領
                reply_text = withdraw._withdraw(command)
            elif command.startswith('deposit'):
                # 充值
                reply_text = deposit._deposit(command)
            elif command.startswith('transfer'):
                # 轉賬
                reply_text = transfer._transfer(command)
            else:
                reply_text = 'Unknown command: [{command}]'
                last_command = copied_command
        logging.info(f'reply_text: [{reply_text}]')
    except Exception as e:
        logging.exception('Got exception on main handler')
        reply_text = f'Exception: {e}'
    return reply_text
