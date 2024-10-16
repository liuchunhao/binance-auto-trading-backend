import requests
import hmac
import hashlib
import time
import logging
import os
import json
from dotenv import load_dotenv


logging.basicConfig(level=logging.INFO, format='%(asctime)s|%(levelname)-8s|%(message)s', datefmt='%Y%m%d %H:%M:%S')

load_dotenv()

class BaseBinanceClient:
    API_KEY = os.getenv('API_KEY', '')
    API_SECRET = os.getenv('API_SECRET', '')
    BASE_URL = 'https://api.binance.com'
    TLD = 'com'
    BASE_URL = f'https://fapi.binance.{TLD}/fapi'
    VERSION = 'v2'

    def __init__(self, api_key=API_KEY, api_secret=API_SECRET, base_url=BASE_URL, version=VERSION) -> None:
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url
        self.version = version
        self.headers = {
            'X-MBX-APIKEY': self.api_key
        }

        # Prepare the request:
        self.timestamp = int(time.time() * 1000)
        self.query_string = f'timestamp={self.timestamp}'
        self.signature = hmac.new(
            self.api_secret.encode('utf-8'), 
            self.query_string.encode('utf-8'), 
            hashlib.sha256
        ).hexdigest()

        logging.info(f'API_KEY={self.api_key}')
        logging.info(f'API_SECRET={self.api_secret}')


    def __signature(self, query_string):
        return hmac.new(
            self.api_secret.encode('utf-8'), 
            query_string.encode('utf-8'), 
            hashlib.sha256
        ).hexdigest()

    def __timestamp(self):
        return int(time.time() * 1000)

    def __query_string(self, **data):
        query_string = f'timestamp={self.__timestamp()}'
        query_string += f'&'.join([f'{key}={value}' for key, value in data.items()])
        query_string += f'&signature={self.__signature(query_string)}'
        return query_string
        
    def __beautify(self, data)->str:
        return json.dumps(data, indent=4, sort_keys=True)

    def get(self, endpoint, version='v2', url=BASE_URL)->requests.Response:
        # url=f'{url}{endpoint}?{query_string}&signature={signature}',
        # url = f'{url}{endpoint}?{self.__query_string()}'
        url = f'{url}/{version}{endpoint}?{self.__query_string()}'
        logging.info(f'GET url: {url}')
        response = requests.get(
            url=url,
            headers=self.headers
        )
        if response.status_code == 200:
            logging.info(f"Success: {response.status_code}")
        else:
            logging.error(f"Failed: {self.__beautify(response.json())}")
        return response

    def post(self, endpoint, data={}, version='v1', url=BASE_URL)->requests.Response:
        url = f'{url}/{version}{endpoint}?{self.__query_string()}'
        logging.info(f'POST url: {url}')
        response = requests.post(
            url=url,
            headers=self.headers,
            data=data
        )
        if response.status_code == 200:
            logging.info(f"Success: {response.status_code}")
        else:
            logging.error(f"Failed: {self.__beautify(response.json())}")
        return response

import binance.client
from typing import Dict

class RevisedBinanceClient(binance.client.Client):
    # enums for API versions
    FUTURES_API_VERSION = 'v1'
    FUTURES_API_VERSION2 = 'v2'

    def futures_account_balance(self, **params):
        """Get futures account balance

        https://binance-docs.github.io/apidocs/futures/en/#future-account-balance-user_data

        """
        return self._request_futures_api('get', 'balance', True, data=params)

    def futures_account(self, **params):
        """Get current account information.

        https://binance-docs.github.io/apidocs/futures/en/#account-information-user_data

        """
        return self._request_futures_api('get', 'account', True, data=params)

    def _request_futures_api(self, method, path, signed=False, **kwargs) -> Dict:
        if kwargs is not None and 'version' in kwargs:
            version = kwargs['version'] 
            uri = self._create_futures_api_uri(path, version=version)
        uri = self._create_futures_api_uri(path)
        return self._request(method, uri, signed, True, **kwargs)

    def _create_futures_api_uri(self, path: str, version = FUTURES_API_VERSION2) -> str:
        url = self.FUTURES_URL
        if self.testnet:
            url = self.FUTURES_TESTNET_URL
        return url + '/' + version + '/' + path

if __name__ == '__main__':
    # response = BaseBinanceClient().get('/sapi/v1/capital/config/getall')
    response = BaseBinanceClient().get(version='v1', endpoint='/account')
    logging.info(f"response: {json.dumps(response.json(), indent=4, sort_keys=True)}")

    response = BaseBinanceClient(base_url='https://www.binance.com/bapi/capital/', version='v1').post(endpoint='/private/capital/withdraw/whitelist/list')
    logging.info(f"response: {json.dumps(response.json(), indent=4, sort_keys=True)}")