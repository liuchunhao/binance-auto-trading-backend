import asyncio
import logging
import json
from datetime import datetime

from websockets import server

from websocket.handler import binance as binance_handler
from websocket.handler import exness as exness_handler

logging.basicConfig(level=logging.INFO)

WEBSOCKET_HOST = "0.0.0.0"
WEBSOCKET_PORT = 8765

# websocket server
async def process(websocket):
    async for message in websocket:
        result = { 
                    "code": 0,
                    "msg": f"success",
                    "data": {},
                    "requestId": "",
                    "timestamp": ""
        }
        try:
            logging.info(f"Received message from client:\n{message}")
            result = __handle(message)
        except Exception as e:
            logging.error(e)
            logging.error(f'processing failed: {e}')
            timestamp = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
            result['code'] = 1
            result['msg'] = f'processing failed: {e}'
            result['data'] = {}
            result['timestamp'] = timestamp
        result = f'{json.dumps(result, indent=4)})'
        await websocket.send(f'{result}')


# parse commnad
def __handle(message):
    '''
    request:
    {
        "command": "withdraw",
        "type": "history",                     # code, history, address
        "args": {
            "network": "ETH",
            "amt": 5
        },
        "timestamp": "2021-07-01 12:00:00"
        "requestId": "1234567890"
    }
    '''
    '''
    result:
    {
        "code": 0,
        "msg": "success",
        "data": {
            "BTC": 0.001,
            "USDT": 100
        },
        "requestId": "1234567890",
        "timestamp": "2021-07-01 12:00:00"
    }
    '''
    request_id = None
    result = { 
                "code": 0,
                "msg": "success",
                "data": {},
                "requestId": request_id,
                "timestamp": f"{datetime.today().strftime('%Y-%m-%d %H:%M:%S')}"
    }

    try: 
        request = json.loads(message)
        command = request['command']
        type = request['type']
        args = request['args']
        logging.info(f'request: {json.dumps(request, indent=4)}')
        if command:
            if not args:
                raise Exception(f'invalid args: {message}') 
            request_id = request['requestId']
            command = command.lower()
            if command == 'withdraw':
                result['data'] = binance_handler.handle_withdraw(args)
            elif command == 'transfer':
                result['data'] = binance_handler.handle_transfer(args)
            elif command == 'order':
                result['data'] = binance_handler.handle_order(args)
            elif command == 'balance':
                result['data'] = binance_handler.handle_balance(args)
            elif command == 'position':
                result['data'] = binance_handler.handle_position(args)
            elif command == 'deposit':
                result['data'] = binance_handler.handle_deposit(args)
            else:
                result['code'] = 1
                result['msg'] = f'unknown command: {message}'
                result['data'] = {}
        else:
            result['code'] = 1
            result['msg'] = f'Invalid command: {message}'
            result['data'] = {}
    except Exception as e:
        logging.error(f'processing failed: {e}')
        result['code'] = 1
        result['msg'] = f'processing failed: {e}'
        result['data'] = {}

    result['requestId'] = request_id
    result['timestamp'] = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    return result


async def main():
    async with server.serve(process, host=WEBSOCKET_HOST, port=WEBSOCKET_PORT):
        await asyncio.Future()          # run forever

def start():
    asyncio.run(main())

