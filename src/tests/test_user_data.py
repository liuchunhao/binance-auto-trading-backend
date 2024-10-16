import sys
import os
# current dir is src/tests, so we need to add src to sys.path to import modules from 'src'
sys.path.append("src")
print(sys.path)
print('current dir: ', os.path.abspath('.'))

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s|%(levelname)-8s|%(message)s', datefmt='%Y%m%d %H:%M:%S')

from common.utils import *
from service.binance.http import balance_service

if __name__ == '__main__':
    # 現貨帳戶餘額 
    result = balance_service.get_spot_balance()
    logging.info(f'result: {beautify_json(result)}')

    # 資金帳戶餘額
    result = balance_service.get_funding_asset()  # DEPRECATED
    logging.info(f'result: {beautify_json(result)}')
    
    # 期貨帳戶餘額
    result = balance_service.get_account_balance()
    logging.info(f'result: {beautify_json(result)}')
