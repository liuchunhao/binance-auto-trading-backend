#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Description: Binance websocket API

import os
import json
import logging
import datetime

import yaml
import requests
from binance import ThreadedWebsocketManager
from binance.client import Client
from dotenv import load_dotenv

from common.constants import Payload            # from src.common.constants import Payload
from common.datetime import render_epoch_time, date_to_epoch, get_days_ago, get_day_count, epoch_to_date
from service.linebot.notification import send_line_notify
from common.utils import beautify_json, format_float

from service.binance.http.client import RevisedBinanceClient

logging.basicConfig(level=logging.INFO, format='%(asctime)s|%(levelname)-8s|%(message)s', datefmt='%Y%m%d %H:%M:%S')
load_dotenv()

api_key = os.getenv('API_KEY')
api_secret = os.getenv('API_SECRET')
num_of_units = int(os.getenv('NUM_OF_UNITS', default='1'))
size_of_contracts = int(os.getenv('SIZE_OF_CONTRACTS', default='1'))
deposit = int(os.getenv('DEPOSIT', default='1'))

logging.info(f'API_KEY={api_key}')
logging.info(f'API_SECRET={api_secret}')
logging.info(f'NUM_OF_UNITS={num_of_units}')
logging.info(f'SIZE_OF_CONTRACTS={num_of_units}')
logging.info(f'DEPOSIT={deposit}')

symbol = 'BNBUSDT'
client = Client(api_key, api_secret)
revised_client = RevisedBinanceClient(api_key, api_secret)

# 設定檔
logging.info(f'search_path: {os.getcwd()}')
with open('src/config.yml', 'r') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
    logging.info(f'config: {config}')


# 1. 前一日資金費率總和
def get_yesterday_funding_fee_sum(symbol):
    from common.datetime import render_epoch_time
    resp = ''
    startTime, fee_sum, fee_list = get_funding_fee_sum(symbol, days=1)
    resp += f'''
    [資金費率]
    合約: {symbol}
    日期: {render_epoch_time(startTime, format='%Y-%m-%d')}
    總計: {format_float(float(fee_sum))}
    分次: {[format_float(float(fee)) for fee in fee_list] }
    '''
    import textwrap
    resp = textwrap.dedent(resp).strip()
    print(resp)
    return resp

# 2. 資金費率總計
def get_funding_fee_sum(symbol, days=300):
    startTime = date_to_epoch(get_days_ago(days))
    eleven_month_ago = date_to_epoch(get_days_ago(335))
    now = date_to_epoch(datetime.datetime.now())
    endTime = now
    funding_fee_history = client.futures_income_history(symbol=symbol, incomeType='FUNDING_FEE', startTime=startTime, endTime=endTime, limit=1000)
    # return startTime, funding_fee_history
    fee_sum = 0
    fee_list = []
    for fee in funding_fee_history:
        logging.info(f'fee: {fee}')
        fee_sum += float(fee['income'])
        fee_list.append(fee['income'])
    return startTime, fee_sum, fee_list

# 3. 資金費率歷史紀錄(Symbol):
def get_funding_fee_history(symbol, days=300):
    startTime = date_to_epoch(get_days_ago(days))

    eleven_month_ago = date_to_epoch(get_days_ago(335))
    now = date_to_epoch(datetime.datetime.now())
    endTime = now

    funding_fee_history = client.futures_income_history(symbol=symbol, incomeType='FUNDING_FEE', startTime=startTime, endTime=endTime, limit=1000)

    # logging.info(f'funding_fee_history: {json.dumps(funding_fee_history, indent=4, sort_keys=True)}')
    total_fee = 0
    count = 0 
    resp = ''

    begin = epoch_to_date(funding_fee_history[0]["time"])
    end = epoch_to_date(funding_fee_history[-1]["time"])
    days = get_day_count(begin, end)

    begin = render_epoch_time(funding_fee_history[0]["time"])
    end = render_epoch_time(funding_fee_history[-1]["time"])

    def get_time_tuple(time):
        return time.year, time.month, time.day, time.hour, time.minute, time.second, time.microsecond

    def get_nearest_lower_number(number, numbers):
        return max(filter(lambda x: x <= number, numbers))
    
    def parse_time(time_string):
        return datetime.datetime.strptime(time_string, '%Y-%m-%d %H:%M:%S')

    def parse_epoch_time(epoch_time):
        return datetime.datetime.fromtimestamp(epoch_time // 1000)
    
    # get datetime that is after 8 hours from specific time
    def get_next_8_hours(time):
        next_8_hours = time + datetime.timedelta(hours=8)
        return datetime.datetime(next_8_hours.year, next_8_hours.month, next_8_hours.day, next_8_hours.hour, 0, 0, 0)

    next_updated_time = 0
    for item in funding_fee_history:
        count += 1
        total_fee += float(item["income"])
        updated_time = parse_epoch_time(item["time"])

        # 計算下次更新時間, 以8小時為單位, 如果不是8小時的倍數, 或是時間不吻合, 就表示沒有資金流水
        while(next_updated_time != 0 and (next_updated_time.day != updated_time.day or next_updated_time.hour != updated_time.hour)):
            _updated_time = next_updated_time
            next_updated_time = get_next_8_hours(next_updated_time)
            resp += f'''
            更新時間: {_updated_time},
            更新時間: {_updated_time.day}, {_updated_time.hour},
            下次更新: {next_updated_time.day}, {next_updated_time.hour},
            合約: {item["symbol"]},
            資金費率: 0 (無資金費率)
            '''

        next_updated_time = get_next_8_hours(updated_time)

        # resp = f'更新時間: {render_epoch_time(item["time"])}, 資產: {item["asset"]}, 合約: {item["symbol"]}, 資金費率: {item["income"]}'
        resp += f'''
        更新時間: {render_epoch_time(item["time"])},
        更新時間: {updated_time.day}, {updated_time.hour},
        下次更新: {next_updated_time.day}, {next_updated_time.hour},
        合約: {item["symbol"]},
        資金費率: {item["income"]}
        '''
    lines = resp.splitlines()
    stripped = [line.strip() for line in lines]
    resp = '\n'.join(stripped)
    logging.info(f'{resp}')
    logging.info(f'total_fee: {total_fee}, count: {count}, begin: {begin}, end: {end}, days: {days}')
    return resp

# 4. 商品最新標記價格(Symbol):
def get_latest_mark_price(symbol):
    mark_price = client.futures_mark_price(symbol=symbol, limit=1)  # 限制回傳筆數
    logging.info(f'mark_price: {json.dumps(mark_price, indent=4, sort_keys=True)}')
    return render_epoch_time(mark_price['time']), float(mark_price['markPrice']) 

# 5. 商品歷史價格(Symbol):
def get_price_history(symbol):
    # startTime = date_to_epoch(get_days_ago(1))
    startTime = date_to_epoch(get_days_ago(30))
    endTime = date_to_epoch(datetime.datetime.now())
    klines = client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1HOUR, startTime, endTime)
    logging.info(f'klines: {json.dumps(klines, indent=4, sort_keys=True)}')

# 6. 取得合約資訊(Symbol):
def get_contract_info(symbol):
    contract_info = client.get_symbol_info(symbol=symbol)
    logging.info(f'contract_info: {json.dumps(contract_info, indent=4, sort_keys=True)}')

# 7. 最新一次資金費率(Symbol):
def get_latest_funding_fee(symbol):
    funding_fee_history = client.futures_income_history(symbol=symbol, incomeType='FUNDING_FEE', startTime=None, endTime=None, limit=None)
    total_fee = 0
    resp = ''
    for item in funding_fee_history[-1:]:
        total_fee += float(item["income"])
        resp += f'''
        更新時間: {render_epoch_time(item["time"])},
        資產: {item["asset"]},
        合約: {item["symbol"]},
        資金費率: {item["income"]}
        '''
    lines = resp.splitlines()
    stripped = [line.strip() for line in lines]
    resp = '\n'.join(stripped)
    logging.info(f'{resp}')
    logging.info(f'total_fee: {total_fee}')
    return resp

# 8. 所有合約最新一次資金費率(Symbol):
def get_total_latest_funding_fee():
    resp = get_latest_funding_fee('BNBUSDT')
    resp += get_latest_funding_fee('BTCUSDT')
    return resp

# 9. 最新一次資金費率(Symbol):
def __latest_funding_fee(symbol):
    resp = get_latest_funding_fee(symbol)
    send_line_notify(f'資金費率:\n{resp}')

# 10. 每日資金費率通知
def latest_funding_fee():
    __latest_funding_fee('BNBUSDT')
    __latest_funding_fee('BTCUSDT')

# 11. 美元匯率
def get_exchange_rate(from_currency='USDT', to_currency='TWD'):
    logging.info(f'get_exchange_rate: from_currency: {from_currency}, to_currency: {to_currency}')
    response = requests.get(f"https://api.exchangerate-api.com/v4/latest/{from_currency}")
    if response.status_code == 200:
        data = response.json()
        logging.info(f'data: {json.dumps(data, indent=4, sort_keys=True)}')
        return data["rates"][to_currency]
    else:
        raise Exception("Error getting exchange rate")


import re
import textwrap
# 12. 取得MT5帳戶資產
def parse_mt5_account_status(text = '''【MT5】
    8點定時回報 
    預付款:4827.00, 淨值:28308.40, 預付款比例:597.25%'''):

    text = textwrap.dedent(text)         # 移除前置空白
    lines = text.splitlines()            # 移除換行, 也會移除換行符號
    non_empty_lines = [line for line in lines if line.strip()]  # 移除空白行
    third_line = non_empty_lines[2]                 # 取得第三行
    logging.info(f'3rd_line: {third_line}')

    # 預付款, 淨值, 預付款比例:
    numbers = re.findall(r'\d+(?:\.\d+)?', third_line)
    logging.info(f'numbers: {numbers}')
    margin, totalMarginBalance = float(numbers[0]), float(numbers[1])
    return margin, totalMarginBalance

# 13. 取得幣安合約帳戶資產
def get_futures_account_status():
    # 初始保證金
    margin = float(config['binance']['futures']['account']['margin'])

    # 美元匯率
    usd_to_twd = get_exchange_rate('USD', 'TWD')

    # 資產
    version = 'v2'
    futures_account = revised_client.futures_account(version=version)  # version=v2
    positions = futures_account['positions']
    position_list = [d for d in positions if d['symbol'] == 'BNBUSDT' or d['symbol'] == 'BTCUSDT']
    logging.info(f'positions: {json.dumps(position_list, indent=4, sort_keys=True)}')

    # 本金 / 美元匯率
    # margin_to_usd = margin / usd_to_twd

    # 最新成交價
    time, bnb_mark_price = get_latest_mark_price('BNBUSDT')
    time, btc_mark_price = get_latest_mark_price('BTCUSDT')

    totalMarginBalance = float(futures_account['totalMarginBalance'])

    # MT5 預付款, 淨值 
    from common.database import select_latest_mt5_balance
    mt5_date, mt5_time, mt5_margin, mt5_total_margin_balance = select_latest_mt5_balance()

    # MT5 + 幣安 淨值
    mt5_and_bn_Balance = mt5_total_margin_balance + totalMarginBalance

    # 單位合約保證金
    margin_per_contract = mt5_and_bn_Balance / size_of_contracts

    # 查詢時間
    from datetime import datetime
    check_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    resp = f''''''

    for position in position_list:
        askNotional = float(position['askNotional'])
        bidNotional = float(position['bidNotional'])
        entryPrice = float(position['entryPrice'])        # 成交價格
        initialMargin = float(position['initialMargin'])  # 初始保證金
        isolated = float(position['isolated'])
        isolatedWallet = float(position['isolatedWallet'])
        leverage = float(position['leverage'])  # 槓桿倍數
        maintMargin = float(position['maintMargin'])
        maxNotional = float(position['maxNotional'])
        notional = float(position['notional'])
        openOrderInitialMargin = float(position['openOrderInitialMargin'])
        positionAmt = float(position['positionAmt'])
        positionInitialMargin = float(position['positionInitialMargin'])
        positionSide = position['positionSide']   # 持倉方向
        symbol = position['symbol']
        unRealizedProfit = float(position['unrealizedProfit'])
        updateTime = position['updateTime']  # 成交時間

        # 最新成交價
        time, mark_price = get_latest_mark_price(symbol)
        check_time = time
        # 市值
        market_value = mark_price * abs(positionAmt)        

        # 槓桿倍數
        leverage = market_value / margin_per_contract

        # 預期合約數量
        expected_leverage = 10
        expected_amt = 10 * margin_per_contract / mark_price

        resp += f'''
        合約: {symbol}
        數量: {positionAmt} 
        現價: {format(mark_price, '.2f')}
        市值: {format(market_value, '.2f')}
        未實現損益: {format(unRealizedProfit, '.2f')}
        槓桿倍數: {format(leverage, '.2f')}
        '''

        # resp += f'''
        # initial_margin: {initialMargin}
        # entry_value: {entryPrice * abs(positionAmt)}
        # '''

        # resp += f'''
        # 更新時間: {time}
        # 預期數量(10x): {format(expected_amt, '.2f')}
        # '''

    availableBalance = float(futures_account['availableBalance'])
    canDeposit = float(futures_account['canDeposit'])
    canWithdraw = float(futures_account['canWithdraw'])
    canTrade = float(futures_account['canTrade'])
    feeTier = float(futures_account['feeTier'])
    maxWithdrawAmount = float(futures_account['maxWithdrawAmount'])
    multiAssetMargin = float(futures_account['multiAssetsMargin'])

    totalCrossUnPnl = float(futures_account['totalCrossUnPnl'])                   # 全倉未實現損益
    totalCrossWalletBalance = float(futures_account['totalCrossWalletBalance'])   # 全倉保證金餘額
    totalInitialMargin = float(futures_account['totalInitialMargin'])             # 帳戶初始保證金
    totalMaintMargin = float(futures_account['totalMaintMargin'])                 # 初始保證金總額
    totalMarginBalance = float(futures_account['totalMarginBalance'])
    totalOpenOrderInitialMargin = float(futures_account['totalOpenOrderInitialMargin']) # 未成交訂單初始保證金
    totalPositionInitialMargin = float(futures_account['totalPositionInitialMargin'])   # 持倉初始保證金
    totalUnrealizedProfit = float(futures_account['totalUnrealizedProfit'])
    totalWalletBalance = float(futures_account['totalWalletBalance'])

    resp += f'''
    未實現損益: {format(totalUnrealizedProfit, '.2f')}
    錢包餘額: {format(totalWalletBalance, '.2f')} 
    保證金餘額: {format(totalMarginBalance, '.2f')}
    '''

    # 本金
    # deposit = 13500 * 2 + 6000 * 2 + (19240 - 500) + (30779 - 80) + 25759

    resp += f'''
    [MT5淨值]
    預付款: {format(mt5_margin, '.2f')}
    淨值: {format(mt5_total_margin_balance, '.2f')}
    最後更新: {mt5_date} {mt5_time}

    [MT5 + 幣安]
    美元匯率: {usd_to_twd}
    本金: {format(deposit, '.2f')}
    淨值: {format(mt5_and_bn_Balance, '.2f')}
    總損益: {format(mt5_and_bn_Balance - deposit, '.2f')} ({format((mt5_and_bn_Balance - deposit) / deposit * 100, '.2f')}%)
    總損益: {format((mt5_and_bn_Balance - deposit) * usd_to_twd, '.2f')} (台幣)
    淨值/{num_of_units}(一份): {format(mt5_and_bn_Balance / num_of_units, '.2f')}(美元)
    淨值/{num_of_units}(一份): {format(mt5_and_bn_Balance / num_of_units * usd_to_twd, '.2f')} (台幣)
    '''

    resp = f'''
    [幣安合約帳戶部位]
    查詢時間: {check_time}
    即時查詢: !position
    {resp}
    '''

    lines = [line.lstrip() for line in resp.splitlines()]
    resp = '\n'.join(lines)
    logging.info(f'futures_account:{resp}')
    return totalMarginBalance, margin, resp

# 14. 合約帳戶資產&餘額不足通知
def futures_account_status():
    totalMarginBalance, margin, resp = get_futures_account_status()
    if totalMarginBalance < margin:
        resp = f'''{resp}\n保證金餘額 < {margin}'''
        # send_line_notify(resp)
    else:
        resp = f'''{resp}\n保證金餘額 > {margin}'''
    logging.info(totalMarginBalance)
    logging.info(margin)
    logging.info(resp)
    return resp

def position_leverage_status():
    # 資產
    version = 'v2'
    futures_account = revised_client.futures_account(version=version)  # version=v2
    positions = futures_account['positions']
    position_list = [d for d in positions if d['symbol'] == 'BNBUSDT' or d['symbol'] == 'BTCUSDT']
    logging.info(f'positions: {json.dumps(position_list, indent=4, sort_keys=True)}')

    for position in position_list:
        positionAmt = round(float(position['positionAmt']), 0)

    # 最新成交價
    time, btc_mark_price = get_latest_mark_price('BTCUSDT')

    totalMarginBalance = round(float(futures_account['totalMarginBalance']), 1)

    margin_call = round(abs(totalMarginBalance / positionAmt), 2)
    leverage = round(abs(btc_mark_price / margin_call), 2)
    return time, positionAmt, totalMarginBalance, btc_mark_price, margin_call, leverage


# 15. 使用 websocket client 接收現貨帳戶餘額 異動通知
def futures_user_socket():
    twm = ThreadedWebsocketManager(api_key=api_key, api_secret=api_secret)
    # start is required to initialise its internal loop
    twm.start()

    def handle_socket_message(msg):
        json_str = json.dumps(msg, indent=4, sort_keys=True)
        logging.info(f"message: {json_str}")

    def handle_margin_socket_message(msg):
        '''
        {
            "e": "marginCall", // Event Type
            "E": 1562305380000, // Event Time
            "cw": "0.02400883", // Cross Wallet Balance
            "p": [ // Position(s)
                {
                "s": "BTCUSDT", // Symbol
                "pa": "1.000", // Position Amount
                "mt": "LONG", // Margin Type
                "iw": "0.00005000", // Isolated Wallet (if isolated position)
                "mp": "9000.00000", // Mark Price
                "up": "-0.09411286", // Unrealized PnL
                "mm": true, // Maintenance Margin Required
                }
            ]
            }
        '''
        logging.info(f"futures_user_socket: {msg[Payload.EVENT_TYPE]}")
        json_str = json.dumps(msg, indent=4, sort_keys=True)
        logging.info(f"message: {json_str}")
        # send_line_notify(json_str)

    # twm.start_user_socket(callback=handle_socket_message)
    twm.start_margin_socket(callback=handle_margin_socket_message)

# 16. 最新的成交價格
def get_latest_price(symbol):
    price = client.get_symbol_ticker(symbol=symbol)
    logging.info(f'price: {json.dumps(price, indent=4, sort_keys=True)}')
    return float(price['price'])


# 17. 成交的上下10檔報價 (max count: 1000)
def get_order_book(symbol):
    depth = client.get_order_book(symbol=symbol, limit=1000)
    '''
        "bids": [ 
        [
            "26007.27000000",   # PRICE
            "0.11867000"        # QTY , unit: BTC
        ],
    '''
    # get depth count of bids and asks
    count = len(depth['bids'])
    update_time = epoch_to_date(depth['lastUpdateId'])
    logging.info(f'order_book(symbol={symbol}, count={count}): {json.dumps(depth, indent=4, sort_keys=True)}')
    return depth
    
# 18. 改用測試網路平倉
def close_position():
    # Q: 測試網路 api key & secret key 需要另外申請嗎？ 
    # A: 不需要, 只要在原本的 api key & secret key 後面加上 -test 就可以了
    
    # 測試網路平倉 
    _client = Client(api_key, api_secret, testnet=True)
    result = _client.futures_create_order(  
        symbol='BTCUSDT',
        side='SELL',
        type='MARKET',
        quantity=0.001,
        positionSide='LONG',
        isIsolated='TRUE',
        reduceOnly='TRUE',
        newOrderRespType='RESULT'
    )


def position_leverage_status():
    # 資產
    version = 'v2'
    futures_account = revised_client.futures_account(version=version)  # version=v2
    positions = futures_account['positions']
    position_list = [d for d in positions if d['symbol'] == 'BNBUSDT' or d['symbol'] == 'BTCUSDT']
    logging.info(f'positions: {json.dumps(position_list, indent=4, sort_keys=True)}')

    for position in position_list:
        positionAmt = round(float(position['positionAmt']), 0)

    # 最新成交價
    time, btc_mark_price = get_latest_mark_price('BTCUSDT')

    totalMarginBalance = round(float(futures_account['totalMarginBalance']), 1)

    margin_call = round(abs(totalMarginBalance / positionAmt), 2)
    leverage = round(abs(btc_mark_price / margin_call), 2)
    return time, positionAmt, totalMarginBalance, btc_mark_price, margin_call, leverage


# Testing
def main():
    # API權限
    account_api_permission = client.get_account_api_permissions()
    logging.info(f"account_api_permission: {json.dumps(account_api_permission, indent=4, sort_keys=True)}")   

    # 帳戶狀態
    account_status = client.get_account_status()
    logging.info(f"account_status: {json.dumps(account_status, indent=4, sort_keys=True)}")

    # 轉賬歷史記錄
    # deposit_history = client.get_deposit_history()
    # logging.info(f'deposit_history: {json.dumps(deposit_history, indent=4, sort_keys=True)}')

    # 轉帳地址
    network = 'TRX' # 'TRC20'
    network = "ETH" # 'ERC20'
    deposit_address = client.get_deposit_address(coin='USDT', network=network)
    logging.info(f'deposit_address: {network}|{json.dumps(deposit_address, indent=4, sort_keys=True)}')

    # 帳戶資產某個時間的快照
    # account_snapshot = client.get_account_snapshot(type='FUTURES', startTime=None, endTime=None, limit=None)
    # logging.info(f'account_snapshot: {json.dumps(account_snapshot, indent=4, sort_keys=True)}')

    # 現貨帳戶資產
    # account = client.get_account()
    # logging.info(f'account: {json.dumps(account, indent=4, sort_keys=True)}')

    # 資金費率歷史記資
    # funding_rate_history = client.futures_funding_rate(symbol=symbol, startTime=None, endTime=None, limit=None)
    # logging.info(f'funding_rate_history: {json.dumps(funding_rate_history, indent=4, sort_keys=True)}')


    # 匯出usdt到MT5地址 : APIError(code=-1002): You are not authorized to execute this request.
    # result = client.withdraw(
    #     coin='USDT',
    #     address='<mt5_address>',
    #     amount=1,
    #     network='TRC20'
    # )
    # logging.info(f'result: {json.dumps(result, indent=4, sort_keys=True)}')
    

    # 資金帳戶轉到現貨帳戶


    # 現貨帳戶轉到資金帳戶


    # 現貨帳戶轉到U本位合約帳戶
    # result = client.sapi_post_futures_transfer(
    #     asset='USDT',
    #     amount=1,
    #     type=1      # 1: transfer from spot account to USDT-Ⓜ futures account. 
    #                 # 2: transfer from USDT-Ⓜ futures account to spot account.
    # )
    # logging.info(f'result: {json.dumps(result, indent=4, sort_keys=True)}')


    # 大戶多空比:
    # futures_top_longshort_account_ratio = client.futures_top_longshort_account_ratio(
    #     symbol='BTCUSDT',
    #     period='5m',
    #     limit=10
    # )
    # logging.info(f'futures_top_longshort_account_ratio: {json.dumps(futures_top_longshort_account_ratio, indent=4, sort_keys=True)}')

    # futures_top_longshort_position_ratio = client.futures_top_longshort_position_ratio (
    #     symbol='BTCUSDT',
    #     period='5m',
    #     limit=10
    # )
    # logging.info(f'futures_top_longshort_position_ratio: {json.dumps(futures_top_longshort_position_ratio, indent=4, sort_keys=True)}')

    # WebSocket 

    twm = ThreadedWebsocketManager(api_key=api_key, api_secret=api_secret)
    # start is required to initialise its internal loop
    # twm.start()

    def handle_socket_message(msg):
        json_str = json.dumps(msg, indent=4, sort_keys=True)
        logging.info(f"message: {json_str}")

    def handle_margin_socket_message(msg):
        '''
        {
            "e": "marginCall", // Event Type
            "E": 1562305380000, // Event Time
            "cw": "0.02400883", // Cross Wallet Balance
            "p": [ // Position(s)
                {
                "s": "BTCUSDT", // Symbol
                "pa": "1.000", // Position Amount
                "mt": "LONG", // Margin Type
                "iw": "0.00005000", // Isolated Wallet (if isolated position)
                "mp": "9000.00000", // Mark Price
                "up": "-0.09411286", // Unrealized PnL
                "mm": true, // Maintenance Margin Required
                }
            ]
            }
        '''
        logging.info(f"futures_user_socket: {msg[Payload.EVENT_TYPE]}")
        json_str = json.dumps(msg, indent=4, sort_keys=True)
        logging.info(f"message: {json_str}")


    def handle_futures_user_socket_message(msg):
        '''
        message type: {
            "E": 1682870400991,
            "T": 1682870400987,
            "a": {
                "B": [
                    {
                        "a": "USDT",
                        "bc": "7.20795369",
                        "cw": "50091.69717692",
                        "wb": "50091.69717692"
                    }
                ],
                "P": [],
                "m": "FUNDING_FEE"
            },
            "e": "ACCOUNT_UPDATE"
        }
        '''
        logging.info(f"futures_user_socket: {msg[Payload.EVENT_TYPE]}")
        json_str = json.dumps(msg, indent=4, sort_keys=True)
        logging.info(f"message: {json_str}")

    def handle_user_socket_message(msg):
        '''
        '''
        logging.info(f"user_socket:")
        json_str = json.dumps(msg, indent=4, sort_keys=True)
        logging.info(f"message: {json_str}")

    def handle_futures_socket_message(msg):
        '''
        '''
        logging.info(f"futures_socket:")
        json_str = json.dumps(msg, indent=4, sort_keys=True)
        logging.info(f"message: {json_str}")
    

    # twm.start_kline_socket(callback=handle_socket_message, symbol=symbol)

    # multiple sockets can be started
    # twm.start_depth_socket(callback=handle_socket_message, symbol=symbol)

    # twm.start_trade_socket(callback=handle_socket_message, symbol=symbol)
    # twm.start_user_socket(callback=handle_socket_message)

    # twm.start_futures_socket(callback=handle_socket_message)
    # twm.start_symbol_ticker_futures_socket(callback=handle_socket_message, symbol=symbol) # bookTicker
    # twm.start_individual_symbol_ticker_futures_socket(callback=handle_socket_message, symbol=symbol) # bookTicker

    # or a multiplex socket can be started like this
    # see Binance docs for stream names
    # streams = ['bnbusdt@ticker', 'btcusdt@ticker']
    streams = ['bnbusdt@miniTicker', 'btcusdt@miniTicker']
    # streams = ['bnbusdt@bookTicker', 'btcusdt@bookTicker']
    # twm.start_multiplex_socket(callback=handle_socket_message, streams=streams) 
    # twm.start_futures_user_socket(callback=handle_futures_user_socket_message) 
    # twm.start_user_socket(callback=handle_user_socket_message)
    # twm.start_futures_socket(callback=handle_futures_socket_message)

    # 收取margin call (餘額不足通知)
    # twm.start_margin_socket(callback=handle_socket_message)

    # 收取MT5轉帳到幣安現貨帳戶通知

    # 收取幣安現貨帳戶轉帳到U本位合約帳戶通知？

    # twm.join()
