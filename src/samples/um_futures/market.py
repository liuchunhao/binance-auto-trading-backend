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

    # 行情訊息Market
    print('## 資金費率')
    fundingRate = binance.um.market.get_fundingRate(symbol='BNBUSDT')  
    print_json(fundingRate)

    epoch_time = int(fundingRate['data'][-1]['fundingTime']) 
    print(epoch_time)
    fundingTime = get_timestamp(epoch_time)
    print(fundingTime)

    ticker_price_bnb = binance.um.market.get_ticker_price(symbol='BNBUSDT')     # 最新價格
    print_json(get_timestamp(ticker_price_bnb['data']['time']))
    print_json(ticker_price_bnb['data']['price'])

    ticker_price_btc = binance.um.market.get_ticker_price(symbol='BTCUSDT')     # 最新價格
    print_json(get_timestamp(ticker_price_bnb['data']['time']))
    print_json(ticker_price_bnb['data']['price'])

    top_long_short_account_ratio = binance.um.market.get_topLongShortAccountRatio(symbol='BTCUSDT', period="5m", limit=30)  # 大戶帳戶數多空比(間隔5分鐘)(最多30筆)
    print_json(top_long_short_account_ratio)
    print_json([ get_timestamp(t['timestamp']) for t in top_long_short_account_ratio['data']] )

    top_long_short_account_ratio = binance.um.market.get_topLongShortAccountRatio(symbol='BNBUSDT', period="5m", limit=30)  # 大戶帳戶數多空比(間隔5分鐘)(最多30筆)
    print_json(top_long_short_account_ratio)
    print_json([ get_timestamp(t['timestamp']) for t in top_long_short_account_ratio['data']] )


