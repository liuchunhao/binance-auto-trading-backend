from service.binance.http import deposit_service
from service.binance.http import withdraw_service
from service.binance.http import transfer_service
from service.binance.http import balance_service

# deposit
def handle_deposit(args):
    '''
    {
        "command": "deposit",
        "type": "address",         
        "args": {
            "network": "TRX"
        },
        "timestamp": "2021-07-01 12:00:00"
        "requestId": "1234567890"
    }
    '''
    network = args['network']
    result = deposit_service.get_deposit_address(network=network)
    return result
    
# withdraw
def handle_withdraw(args):
    '''
    {
        "command": "withdraw",
        "type": "code",         # code, history, address
        "args": {
            "network": "ETH",
            "amt": 5
        },
        "timestamp": "2021-07-01 12:00:00"
    }
    '''
    result = withdraw_service.withdraw(args)
    return result

# transfer
def handle_transfer(args):
    '''
    {
        "command": "transfer",
        "args": {
            "from": "spot",
            "to": "futures",
            "amt": 5
        },
        "timestamp": "2021-07-01 12:00:00"
    }
    '''
    amt=int(args['amt'])
    __from = args['from']
    __to = args['to']
    
    result = 'Not implemented'
    if __from == 'spot' and __to == 'futures':
        result = transfer_service.spot_transfer_to_futures(amt)
    elif __from == 'futures' and __to == 'spot':
        result = transfer_service.futures_transfer_to_spot(amt)
    return result

# order
def handle_order(args):
    '''
    {
        "command": "order",
        "args": {
            "type": "limit",
            "symbol": "btcusdt",
            "amt": 0.001,
            "side": "sell",
            "price": 32000
        },
        "timestamp": "2021-07-01 12:00:00",
        "requestId": "1234567890"
    }
    '''
    result = 'Not implemented'
    return result

# balance
def handle_balance(args):
    '''
    {
        "command": "balance",
        "type": "",
        "args": {
            "type": "spot"
        },
        "timestamp": "2021-07-01 12:00:00",
        "requestId": "1234567890"
    }
    '''
    result = 'Not implemented'
    
    result = balance_service.get_spot_balance()
    return result

# position
def handle_position(args):
    '''
    {
        "command": "position",
        "args": {
            "symbol": "btcusdt"
        },
        "timestamp": "2021-07-01 12:00:00",
        "requestId": "1234567890"
    }
    '''
    '''
    {
        "code": 0,
        "msg": "success",
        "data": {
            "binance": {
                "symbol": "BTCUSDT",
                "position": 0.001,
                "price": 32000
            },
            "exness": {
                "symbol": "btcusdt",
                "position": 0.001,
                "price": 32000
            }
        },
        "requestId": "1234567890",
        "timestamp": "2021-07-01 12:00:00"
    }
    '''
    result = ''
    return result
