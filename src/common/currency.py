import json
import logging
import requests

from common.datetime import *

logging.basicConfig(level=logging.INFO)

# check out here: https://app.exchangerate-api.com/dashboard
API_KEY = '43239fc2023fdcf43377e298'

# get currency rate: 
# 1. The data only refreshes once every 24 hours anyway
# 2. 1500 requests p/m
def get_currency_rate(base='USD', target='TWD'):
    url = f'https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{base}'
    response = requests.get(url)
    data = json.loads(response.text)
    logging.info(f'get_currency_rate(base={base}, target={target}): {json.dumps(data, indent=4, sort_keys=True)}')
    
    return f'''
    from: {data['base_code']} 
    to: {target} {data['conversion_rates'][target]} 
    last_update:  {data['time_last_update_utc']} 
    '''
