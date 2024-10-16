import sys
import os
# current dir is src/tests, so we need to add src to sys.path to import modules from 'src'
sys.path.append("src")
print(sys.path)
print('current dir: ', os.path.abspath('.'))

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s|%(levelname)-8s|%(message)s', datefmt='%Y%m%d %H:%M:%S')

from common.utils import *
from common.database import *
from service.binance import user_data
from service.binance.http import transfer_service
from service.binance.http import balance_service

if __name__ == '__main__':
    # 1. 轉帳
    # 1.1 合約->現貨
    # tranId = user_data.futures_transfer_to_spot(amount='1')

    # 1.2 現貨->合約s
    # tranId = user_data.spot_transfer_to_futures(amount='1')
    # user_data.get_transfer_history_by_tranId(tranId)
    # user_data.get_spot_balance()

    # 1.3 轉帳歷史紀錄 
    # user_data.get_transfer_history_list(days=1)
    result = transfer_service.get_transfer_history_list(days=100)
    logging.info(f'result: {beautify_json(result)}')

