import logging
import json
import time
import datetime

from flask import Blueprint
from flask import request, abort, g

from service.linebot import notification
from service.binance import user_data
from common import database
from service.discord.webhook import secret, warning

from dotenv import load_dotenv
import os

load_dotenv()

MOBILE_HEARTBEAT_INTERVAL = int(os.getenv('SMS_APP_MOBILE_HB_INTERVAL', default=900))

MOBILE_LIST = []
MOBILE_HEARTBEAT_TIMESTAMP = {}

mobile_env = os.getenv('SMS_APP_MOBILE_LIST')
if mobile_env is not None and mobile_env.strip() != '':
    mobile_env = mobile_env.strip()
    if ',' in mobile_env:
        MOBILE_LIST = mobile_env.split(',')
    else:
        MOBILE_LIST.append(mobile_env)

logging.basicConfig(level=logging.INFO, format='%(asctime)s|%(levelname)-8s|%(message)s', datefmt='%Y%m%d %H:%M:%S')

URL_PREFIX = '/api/v1/exness'

bp = Blueprint('exness_controller', __name__, url_prefix=URL_PREFIX)

sms = {
    'timestamp': '2021-08-01 12:00:00',
    'mobile': '+886 0912345678',
    'verfication_code': '123456'
}

def check_mobile_alive():
    logging.info(f'Start checking mobile heartbeat !')
    while True:
        logging.info(f'Checking mobile heartbeat...{MOBILE_HEARTBEAT_TIMESTAMP}')
        logging.info(f'Checking mobile heartbeat...{MOBILE_LIST}')

        for mobile in MOBILE_LIST:
            if mobile == '':
                continue
            if MOBILE_HEARTBEAT_TIMESTAMP.get(mobile) is None:
                MOBILE_HEARTBEAT_TIMESTAMP[mobile] = time.time()
                logging.info(f'[{mobile}] heartbeat initialized: {MOBILE_HEARTBEAT_TIMESTAMP[mobile]}')
                continue
            else:
                timestamp = datetime.datetime.fromtimestamp(MOBILE_HEARTBEAT_TIMESTAMP[mobile]).strftime('%Y-%m-%d %H:%M:%S')
                logging.info(f'[{mobile}] heartbeat last updated: timestamp={timestamp}')
                diff = int(time.time() - MOBILE_HEARTBEAT_TIMESTAMP[mobile])

                if diff > MOBILE_HEARTBEAT_INTERVAL:
                    logging.info(f'[{mobile}] heartbeat expired: {diff} > {MOBILE_HEARTBEAT_INTERVAL}')
                    warning.send(f'[{mobile}] heartbeat expired: {diff} > {MOBILE_HEARTBEAT_INTERVAL}')

        time.sleep(60)


def log_decorator(func):
    def wrapper(*args, **kwargs):
        logging.info(f"args: {args}, kwargs: {kwargs}")
        result = func(*args, **kwargs)
        logging.info(f"result: {result}")
    return wrapper

def render_err(e: Exception):
    return {
        "timestamp": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
        "code": -1,
        "msg": f"Exception: {e}"
    }

@log_decorator
@bp.route("/sms/verificationCode", methods=['GET'])
def get_sms():
    logging.info(f"GET|{URL_PREFIX}/sms")
    try:
        return {
           "timestamp": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
           "code": 0,
           "msg": "GET Exness verification code successfully",
           "data": {
               "timestamp": sms['timestamp'],  
               "mobile": sms['mobile'],
               "verfication_code": sms['verfication_code']
           }
        }
    except Exception as e:
        logging.error(f"Exception: {e}")
        return render_err(e)


@log_decorator
@bp.route("/sms", methods=['POST'])
def sms_post():
    '''
    # 1. Exness SMS:
        {
            "timestamp": "2021-08-01 12:00:00",
            "mobile": "+886 0912345678",
            "msg": "Your Exness verification code is: 123456"
        }


    # 2. Binance SMS:
        "[Binance] Verification code: 363688. You are trying to change your phone number. Beware of scam calls and SMS phishing and verify sources with Binance Verify"

    '''
    try:
        logging.info(f"POST|{URL_PREFIX}/sms|payload:[{request.get_data(as_text=True)}]")
        payloads = request.get_data(as_text=True).replace('\r', '').replace('\n', '').strip()
        body = json.loads(payloads)

        timestamp = body['timestamp']
        mobile = body['mobile']
        msg = body['msg']
        where = ''
        code = '000000'

        if 'Exness' in msg:
            code = str(msg.split(':')[1]).strip()
            where = 'Exness'
        elif 'Binance' in msg:
            code = str(msg.split(':')[1]).split('.')[0].strip()
            where = 'Binance'

        sms['timestamp'] = timestamp
        sms['mobile'] = mobile
        sms['verfication_code'] = code

        # send to discord webhook
        if code != '000000':
            secret.send(f'[{where}] verification code on mobile [{mobile}] is: [{code}]')

        return {
           "timestamp": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
           "code": 0,
           "msg": "verification code sent successfully" if code != '000000' else "verification code not found",
           "data": {
               "timestamp": sms['timestamp'],  
               "mobile": sms['mobile'],
               "verfication_code": sms['verfication_code']
           }
        }
    except Exception as e:
        logging.error(f"Exception: {e}")
        return render_err(e)


@bp.route("/ping", methods=['GET'])
def ping():
    logging.info(f"GET|{URL_PREFIX}/ping")
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    
    return {
        "timestamp": timestamp,
        "code": 0,
        "msg": "pong"
    }


@bp.route("/heartbeat", methods=['POST'])
def heartbeat():
    '''
        {
            "timestamp": "2021-08-01 12:00:00",
            "mobile": "+886910111222
        }
    
    '''
    try: 
        logging.info(f"POST|{URL_PREFIX}/heartbeat|payload:[{request.get_data(as_text=True)}]")
        payloads = request.get_data(as_text=True).replace('\r', '').replace('\n', '').strip()
        body = json.loads(payloads)

        timestamp = body['timestamp']
        mobile = body['mobile']

        # put UTC+0 time into MOBILE_HEARTBEAT_TIMESTAMP
        MOBILE_HEARTBEAT_TIMESTAMP[mobile] = time.time()

        return {
            "timestamp": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
            "code": 0,
            "msg": "success"
        }

    except Exception as e:
        logging.error(f"Exception: {e}")
        return render_err(e)


    