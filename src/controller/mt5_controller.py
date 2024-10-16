import logging
import json

from flask import Blueprint
from flask import request, abort, g

from service.linebot import notification
from service.binance import user_data
from common import database

logging.basicConfig(level=logging.INFO, format='%(asctime)s|%(levelname)-8s|%(message)s', datefmt='%Y%m%d %H:%M:%S')

bp = Blueprint('mt5_controller', __name__)

@bp.route('/linebot')
def index():
    return "Hello from linebot_controller!"

def log_decorator(func):
    def wrapper(*args, **kwargs):
        logging.info(f"args: {args}, kwargs: {kwargs}")
        result = func(*args, **kwargs)
        logging.info(f"result: {result}")
    return wrapper

@log_decorator
@bp.route("/api/v1/mt5_balance", methods=['GET'])
def mt5_balance_get():
    try:
        logging.info(f"GET|mt5_balance_get: [{request.args}]")
        '''
        https://c3ad-61-222-207-211.ngrok-free.app/mt5_balance?balance=1000&margin=200
        '''
        # path variables
        margin = str(request.args.get('margin')).replace('\r', '').replace('\n', '').strip()
        balance = str(request.args.get('balance')).replace('\r', '').replace('\n', '').strip()

        # str -> float
        margin = float(str(margin))
        balance = float(str(balance))

        # save to database
        database.insert_mt5_balance(margin=margin, balance=balance)  
        logging.info(f"balance: {balance}, margin: {margin}")

        # summary for futures account status
        total_margin_balance, bnc_margin, reply_text = user_data.get_futures_account_status()

        # send notification via LINE
        resp = f'收到MT5通知:\n{reply_text}'
        notification.send_line_notify(resp)
    except Exception as e:
        logging.error(f"Exception: {e}")
        return f"Exception: {e}"
    return f"received: margin:{margin}, balance:{balance}"


@log_decorator
@bp.route("/api/v1/mt5_balance", methods=['POST'])
def mt5_balance_post():
    try:
        logging.info(f"POST:mt5_balance_post: [{request.get_data(as_text=True)}]")
        payloads = request.get_data(as_text=True).replace('\r', '').replace('\n', '').strip()
        body = json.loads(payloads)
        margin = body['margin']
        balance = body['balance']
        '''
        {
            "balance": 1000,
            "margin": 200
        }
        
        '''

        # validate margin and balance is number
        # if not re.match(r'^-?\d+(?:\.\d+)?$', str(margin)):
        #     return "margin is not number"
        # if not re.match(r'^-?\d+(?:\.\d+)?$', str(balance)):
        #     return "balance is not number"

        # insert to database
        database.insert_mt5_balance(margin=margin, balance=balance)
        logging.info(f"balance: {balance}, margin: {margin}")

        # send line notify
        total_margin_balance, bnc_margin, reply_text = user_data.get_futures_account_status()
        resp = f'收到MT5通知:\n{reply_text}'
        notification.send_line_notify(resp)
    except Exception as e:
        logging.error(f"Exception: {e}")
        return f"Exception: {e}"
    return f"received: balance:{body['balance']}, margin:{body['margin']}"

