# exness

# price divergence
def __handle_exness_mark_price_div(args):
    '''
    {
        "command": "exness",
        "type": "mark_price",
        "args": {
            "symbol": "btcusdt"
            "price": 32000
        },
        "timestamp": "2021-07-01 12:00:00",
        "requestId": "1234567890"
    }
    '''
    result = {
        "code": 0,
        "msg": "success",
        "data": {
            "exness": {
                "symbol": "btcusdt",
                "price": 32000
            },
            "binance": {
                "symbol": "BTCUSDT",
                "price": 32000
            },
            "divergence": 0.001
        },
        "requestId": "1234567890",
        "timestamp": "2021-07-01 12:00:00"
    }
    return result


# futures position
def __handle_exness_position(args):
    '''
    {
        "command": "exness",
        "type": "position",
        "args": { },
        "timestamp": "2021-07-01 12:00:00",
        "requestId": "1234567890"
    }
    '''
    result = {
        "code": 0,
        "msg": "success",
        "data": {
            "exness": {
                "symbol": "BTCUSDT",
                "side": "BUY",
                "amt": 1.5,
                "unrealizedPnl": -99.99,
            },
            "binance": {
                "symbol": "BTCUSDT",
                "side": "SELL",
                "amt": 2.5,
                "unrealizedPnl": 999.99,
            }
        },
    }
    return result
    

# spot balance
def __handle_exness_spot_balance(args):
    '''
    {
        "command": "exness",
        "type": "spot_balance",
        "args": { },
        "timestamp": "2021-07-01 12:00:00",
        "requestId": "1234567890"
    }
    
    '''
    result = {
        "code": 0,
        "msg": "success",
        "data": {
            "exness": {
                "wallet": 9.99,
            },
            "binance": {
                "wallet": 9.99,
            }
        },
    }
    return result


# balance
def __handle_exness_balance(args):
    '''
    {
        "command": "exness",
        "type": "balance",
        "args": { },
        "timestamp": "2021-07-01 12:00:00",
        "requestId": "1234567890"
    }
    '''
    result = {
        "code": 0,
        "msg": "success",
        "data": {
            "exness": {
                "wallet": 9.99,
                "margin": 999.99
            },
            "binance": {
                "wallet": 9.99,
                "margin": 999.99
            }
        },
    }
    return result

# order
def __handle_exness_order(args):
    '''
    {
        "command": "exness",
        "type": "order",
        "args": { },
        "timestamp:: "2021-07-01 12:00:00",
        "requestId: "1234567890"
    }
    
    '''
    result = {
        "code": 0,
        "msg": "success",
        "data": {
            "exness": {
                "symbol": "BTCUSDT",
                "side": "BUY",
                "amt": 1.5,
                "price": 32000,
            },
            "binance": {
                "symbol": "BTCUSDT",
                "side": "SELL",
                "amt": 2.5,
                "price": 32000,
            }
        },
    }
    return result