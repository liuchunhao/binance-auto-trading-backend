import requests
import hmac
import hashlib
import time
import logging
from dotenv import load_dotenv
import os


logging.basicConfig(level=logging.INFO, format='%(asctime)s|%(levelname)-8s|%(message)s', datefmt='%Y%m%d %H:%M:%S')
load_dotenv()

API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')
if not API_KEY or not API_SECRET:
    logging.error(f'API_KEY or API_SECRET is empty. Please check .env file.')
    exit(1)

logging.info(f'API_KEY={API_KEY}')
logging.info(f'API_SECRET={API_SECRET}')

BASE_URL = 'https://api.binance.com'

# Prepare the request
timestamp = int(time.time() * 1000)
query_string = f'timestamp={timestamp}'
signature = hmac.new(
    API_SECRET.encode('utf-8'), 
    query_string.encode('utf-8'), 
    hashlib.sha256
).hexdigest()

headers: dict = {
    'X-MBX-APIKEY': API_KEY
}

def get(endpoint, url=BASE_URL):
    response = requests.get(
        f'{url}{endpoint}?{query_string}&signature={signature}',
        headers=headers
    )
    if response.status_code == 200:
        data = response.json()
        print(f"Supported coins: {data}")
    else:
        print(f"Failed to get supported coins. Error code: {response.status_code}")
    return response

def post(endpoint, url=BASE_URL):
    response = requests.post(
        f'{url}{endpoint}?{query_string}&signature={signature}',
        headers=headers
    )
    if response.status_code == 200:
        data = response.json()
        print(f"Supported coins: {data}")
    else:
        print(f"Failed to get supported coins. Error code: {response.status_code}")
    return response


if __name__ == '__main__':
    get('/sapi/v1/capital/config/getall')
