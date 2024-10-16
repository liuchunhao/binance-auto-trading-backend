import sys
import os
# current dir is src/tests, so we need to add src to sys.path to import modules from 'src'
sys.path.append("src")
print(sys.path)
print('current dir: ', os.path.abspath('.'))

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s|%(levelname)-8s|%(message)s', datefmt='%Y%m%d %H:%M:%S')

from common.utils import beautify_json
from service.binance.http import withdraw_service
from service.binance.http.client import BaseBinanceClient

if __name__ == '__main__':

    # 出金 (be careful, it's real money)
    # withdraw.withdraw(network='TRX', address='', amount=0.1)
    
    # 出金歷史紀錄
    result: dict = withdraw_service.get_withdraw_history(offset=0, limit=10)
    logging.info(f'result: {beautify_json(result)}')

    # 出金狀態碼
    result: dict = withdraw_service.get_withdraw_status_code()
    logging.info(f'result: {beautify_json(result)}')

    # withdraw whitelist (does not work)
    # import json
    # client = BaseBinanceClient(base_url='https://www.binance.com/bapi/capital', version='v1')
    # response = client.post(url='https://www.binance.com/bapi/capital', version='v1', endpoint='/private/capital/withdraw/whitelist/list')
    # logging.info(f"response: {json.dumps(response.json(), indent=4, sort_keys=True)}")