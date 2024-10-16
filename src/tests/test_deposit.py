import sys
import os
# current dir is src/tests, so we need to add src to sys.path to import modules from 'src'
sys.path.append("src")
print(sys.path)
print('current dir: ', os.path.abspath('.'))

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s|%(levelname)-8s|%(message)s', datefmt='%Y%m%d %H:%M:%S')

from common.utils import beautify_json
from service.binance.http import deposit_service

if __name__ == '__main__':
    # 1. deposit addres (入金錢包地址)
    result = deposit_service.get_deposit_address(network='TRX')
    logging.info(f'result: {beautify_json(result)}')

    # 2. deposit history (入金歷史記錄)
    result = deposit_service.get_deposit_history(offset=0, limit=1)
    logging.info(f'result: {beautify_json(result)}')
