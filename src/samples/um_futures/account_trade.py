# -*- coding: utf-8 -*-
from pbinance import Binance, UM
import json
import datetime
import time

API_KEY = '1XHbm0oQXt0ocT4NlSEsejfyLhnErejQXqcOxGdVTAE1I0XyZNgkdXFhF4ojmksw'
SECRET_KEY = 'O7F7iXmMKFhXLwwIPfhKBMxo9yOsD5GjmgafzYEkMoDvK4C13PbqF7ei2qCmGT1c'

# 從list中取出指定key包含某個value的dict (用map的方式)
def get_dict_from_list_by_key_value(data_list, key, value):
    return data_list.map(lambda x: x if x[key] == value else None)

def get_timestamp(epoch_time, timezone=8, ms=1000):
    epoch_time = int(epoch_time) // ms                             # 毫秒轉秒
    tz = datetime.timezone(datetime.timedelta(hours=timezone))     # UTC+8
    return datetime.datetime.fromtimestamp(epoch_time, tz=tz).strftime('%Y-%m-%d %H:%M:%S')

def print_json(data):
    print(json.dumps(data, indent=4, sort_keys=True))

# write json to file
def write_json_to_file(data, file_name):
    with open(file_name, 'w') as f:
        json.dump(data, f, indent=4, sort_keys=True)

if __name__ == '__main__':

    # account's key & secret
    binance = Binance(
        key=API_KEY,
        secret=SECRET_KEY
    )
    depth = binance.um.market.get_depth(symbol='BNBUSDT')
    print(json.dumps(depth, indent=4, sort_keys=True))

    # 帳戶與交易資訊
    
    print('## 資產餘額: ')
    balance = binance.um.accountTrade.get_balance()     
    # print(json.dumps(balance, indent=4, sort_keys=True))
    
    balance = [b for b in balance['data'] if b['asset'] == 'USDT'][0]
    print_json(balance)
    print(get_timestamp(balance['updateTime']))
    
    print('## 帳戶資訊: ')
    account = binance.um.accountTrade.get_account()
    print_json(account)
    write_json_to_file(account, 'data/account.json')
    positions = [a for a in account['data']['positions'] if a['symbol'] == 'BTCUSDT' or a['symbol'] == 'BNBUSDT']
    print('## 部位資訊: ')
    print_json(positions)


    
    # 
    # transform timestamp to datetime
    # for fundingTime in datetime.datetime.fromtimestamp(fundingRate['fundingTime']):
    #     print(fundingRate)
    
    # um = UM(key=API_KEY, secret=SECRET_KEY)
    # result = um.accountTrade.get_balance()
    # result = um.portfolioMargin.get_pmAccountInfo(asset='BNBUSDT')
    # print(json.dumps(result, indent=4, sort_keys=True))

