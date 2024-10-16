from service.binance.http import futures_service
import json

# 1. 合約下單/刪單/平倉/查詢
def _create_order(command):
    '''
        下單
        ! order limit: symbol=btcusdt, amt=0.01, side=sell, price=30000
        ! order market: symbol=btcusdt, amt=0.01, side=sell

        刪單
        ! order cancel: symbol=btcusdt, orderId=123456

        平倉
        ! order close: symbol=btcusdt

        委託查詢
        ! order status
        ! order status: symbol=btcusdt
        ! order status: symbol=bnbusdt, orderId=123456
    '''
    reply_text = 'Not implemented yet'
    result = ''
    commands = command.split(':')
    if len(commands) >= 2:
        type = commands[0].split('order')[1].strip()
        args = commands[1].split(',')
        args = [ arg.strip() for arg in args if arg != '' ]
        symbol, orderId, amt, side, price = '', 0, '', '', 0
        for arg in args:
            key_value = arg.split('=')
            if len(key_value) == 2:
                key = key_value[0]
                value = key_value[1]
                if key == 'symbol':
                    symbol = value.upper()
                elif key == 'amt':
                    amt = value
                elif key == 'side':
                    side = value.upper()
                elif key == 'price':
                    price = value
                elif key == 'orderId':
                    orderId = value

        if type == 'limit':
            # 現價單
            reply_text = f'order {type}: symbol={symbol}, amt={amt}, side={side}, price={price}'
            futures_service.limit_order(symbol=symbol, side=side, quantity=amt, price=price)
        elif type == 'market':
            # 市價單
            reply_text = f'order {type}: symbol={symbol}, amt={amt}, side={side}'
            # result = futures_create_market_order(symbol=symbol, side=side, quantity=amt)
            result = f'Not implemented yet'
        elif type == 'cancel':
            # 刪單
            if orderId == '':
                # 刪除全部委託
                reply_text = f'order {type}: symbol={symbol}'
                result = futures_service.futures_cancel_all_open_orders(symbol=symbol)
            else:   
                reply_text = f'order {type}: symbol={symbol}, orderId={orderId}'
                result = futures_service.futures_cancel_order(symbol=symbol, orderId=orderId)
        elif type == 'close':
            # 平倉
            reply_text = f'order {type}: symbol={symbol}'
            result = f'Not implemented yet'
        elif type == 'status':
            # 歷史委託查詢
            reply_text = f'order {type}: symbol={symbol}, orderId={orderId}'
            if orderId:
                result = futures_service.futures_get_order_by_orderId(symbol=symbol, orderId=orderId)
            else:
                result = futures_service.futures_cancel_all_open_orders(symbol=symbol)
        else:
            reply_text = 'Unknown command: order {type}'
    elif len(commands) == 1:
        type = commands[0].split('order')[1].strip()
        if type == 'status':
            # 委託查詢(全部)
            result = futures_service.futures_get_all_open_orders()
            reply_text = f'{json.dumps(result, indent=4, sort_keys=True)}'
        else:
            reply_text = 'Unknown command: [order {type}]'
    else:
        reply_text = 'Unknown command: [{command}]'
        
    reply_text = f'{reply_text} -> result={json.dumps(result, indent=4, sort_keys=True)}'
    return reply_text