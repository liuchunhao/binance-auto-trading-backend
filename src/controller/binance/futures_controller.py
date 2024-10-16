import logging
import json

from flask import Blueprint, request, jsonify
from flask_cors import cross_origin

from service.binance.http import futures_service
from model.r import R
from common.datetime import render_epoch_time

# Futures API
bp = Blueprint('futures_controller', __name__, url_prefix='/futures') 


# GET / Balance
@bp.route('/history/trades', methods=['GET'], )
@cross_origin() 
def get_account_balance():
    symbol = request.args.get('symbol')
    limit = request.args.get('limit', default=10, type=int)
    result = futures_service.account()
    return R.success(result).to_json()


# GET / Position 
@bp.route('/position', methods=['GET'], )
@cross_origin() 
def get_future_position():
    result = futures_service.futures_position()
    result = [item for item in result if float(item['positionAmt']) != 0]
    result = [dict(item, **{'updateTime': render_epoch_time(item['updateTime'])}) for item in result]   
    return R.success(result).to_json()


# GET / All Open Orders
@bp.route('/order', methods=['GET'], )
@cross_origin() 
def get_all_open_orders():
    result = futures_service.futures_get_all_open_orders()
    result = [dict(item, **{'updateTime': render_epoch_time(item['updateTime']), 'orderId': str(item['orderId'])}) for item in result]   
    return R.success(result).to_json()


# POST / New Order
@bp.route('/order', methods=['POST'])
@cross_origin() 
def _order():
    payload = request.get_json()
    if not payload:
        return jsonify({'error': 'Please provide a valid JSON payload.'}), 400
    symbol = payload['symbol']
    side = payload['side']
    type = payload['type']
    quantity = payload['quantity']
    price = payload['price']
    timeInForce = payload['timeInForce']

    result = futures_service.futures_create_order(symbol=symbol, type=type, side=side, quantity=quantity, price=price, timeInForce=timeInForce)
    result = dict(result, **{'updateTime': render_epoch_time(result['updateTime']), 'orderId': str(result['orderId']) })
    return R.success(result).to_json()


# POST / Limit Order
@bp.route('/limitOrder', methods=['POST'])
@cross_origin() 
def limit_order():
    payload = request.get_json()
    if not payload:
        return jsonify({'error': 'Please provide a valid JSON payload.'}), 400  # check if not exist, return 400

    symbol = payload['symbol']
    side = payload['side']
    quantity = payload['quantity']
    price = payload['price']

    result = futures_service.limit_order(symbol=symbol, side=side, quantity=quantity, price=price)
    result = dict(result, **{'updateTime': render_epoch_time(result['updateTime']), 'orderId': str(result['orderId']) })
    return R.success(result).to_json()


# POST / Market Order
@bp.route('/marketOrder', methods=['POST'])
@cross_origin() 
def market_order():
    payload = request.get_json()
    if not payload:
        return jsonify({'error': 'Please provide a valid JSON payload.'}), 400  # check if not exist, return 400
    symbol = payload['symbol']
    side = payload['side']
    quantity = payload['quantity']

    result = futures_service.market_order(symbol=symbol, side=side, quantity=quantity)
    result = dict(result, **{'updateTime': render_epoch_time(result['updateTime']), 'orderId': str(result['orderId']) })
    return R.success(result).to_json()


# POST / Stop Limit
@bp.route('/stopLimitOrder', methods=['POST'])
@cross_origin() 
def stop_limit():
    payload = request.get_json()
    if not payload:
        return jsonify({'error': 'Please provide a valid JSON payload.'}), 400

    symbol = payload['symbol']
    side = payload['side']
    quantity = payload['quantity']
    stopPrice = payload['stopPrice']
    price = payload['price']

    result = futures_service.stop_limit(symbol, side, stopPrice, price, quantity)
    result = dict(result, **{'updateTime': render_epoch_time(result['updateTime']), 'orderId': str(result['orderId']) })
    return R.success(result).to_json()


# POST / Stop Market
@bp.route('/stopMarketOrder', methods=['POST'])
@cross_origin() 
def stop_market():
    payload = request.get_json()
    if not payload:
        return jsonify({'error': 'Please provide a valid JSON payload.'}), 400

    symbol = payload['symbol']
    side = payload['side']
    quantity = payload['quantity']
    stopPrice = payload['stopPrice']
    result = futures_service.stop_market(symbol, side, stopPrice, quantity)
    result = dict(result, **{'updateTime': render_epoch_time(result['updateTime']), 'orderId': str(result['orderId']) })
    return R.success(result).to_json()



# PUT / Modify Order
@bp.route('/order', methods=['PUT'])
@cross_origin() 
def modify_order():
    payload = request.get_json()
    orderId = payload['orderId']
    symbol = payload['symbol']
    side = payload['side']
    price = payload['price']
    quantity = payload['quantity']
    logging.info(f'payload: {json.dumps(payload, indent=4, sort_keys=True)}')
    result = futures_service.modify_order(orderId=orderId, symbol=symbol, side=side, quantity=quantity, price=price)
    result = dict(result, **{'updateTime': render_epoch_time(result['updateTime'])})
    return R.success(result).to_json()


# DELETE / Cancel All Orders
@bp.route('/order/all', methods=['DELETE'])
@cross_origin() 
def cancel_all():
    payload = request.get_json()
    symbol = payload['symbol']
    result = futures_service.futures_cancel_all_open_orders(symbol=symbol)
    return R.success(result).to_json()
          

# DELETE / Cancel Order by ID
@bp.route('/order', methods=['DELETE'])
@cross_origin() 
def cancel_by_id():
    payload = request.get_json()
    symbol = payload['symbol']
    orderId = payload['orderId']
    result = futures_service.futures_cancel_order(symbol=symbol, orderId=orderId)
    return R.success(result).to_json()


# GET / Trade List
@bp.route('/trades', methods=['GET'])
@cross_origin()
def get_trade_list():
    symbol = request.args.get('symbol')
    limit = request.args.get('limit', default=10, type=int)
    result = futures_service.futures_account_trades(symbol=symbol, limit=limit)
    result = [dict(item, **{'time': render_epoch_time(item['time']), 'orderId': str(item['orderId']) }) for item in result]   
    return R.success(result).to_json()

