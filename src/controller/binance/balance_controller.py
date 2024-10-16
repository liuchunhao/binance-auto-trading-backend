from flask import Blueprint
from flask_cors import cross_origin
import json
import logging

from service.binance.http import balance_service
from common.datetime import render_epoch_time
from model.r import R

bp = Blueprint('balance_controller', __name__, url_prefix='/balance') # balance_controller is the name of this controller

# 帳號
@bp.route('/account', methods=['GET'])
@cross_origin()
def account_status():
    result, resp = balance_service.get_account_balance()
    return { 
        "code": 0,
        "msg": "success",
        "data": result
    }
    

@bp.route('/futures', methods=['GET'])
@cross_origin()
def balance_futures():
    """Get balance of futures account

    Returns:
        str : json string with data field as follows:

    {
        "accountAlias": "FzuXFzSgsRXquXoC",
        "asset": "USDT",
        "availableBalance": "13841.31975383",
        "balance": "111849.09307806",
        "crossUnPnl": "-83909.14295616",
        "crossWalletBalance": "111849.09307806",
        "marginAvailable": true,
        "maxWithdrawAmount": "13841.31975383",
        "updateTime": 1704898425875,
        "marginBalance": "27940.09307806",  // user defined
    }
    """
    result  = balance_service.get_futures_balance()
    result = [item for item in result if float(item['updateTime']) != 0]
    result = [dict(item, **{'updateTime': render_epoch_time(item['updateTime'])}) for item in result]
    result= [dict(item, **{'marginBalance': str(float(item['balance']) + float(item['crossUnPnl']))}) for item in result]
    logging.info(f'balance_futures: {json.dumps(result, indent=4, sort_keys=True)}')
    return R.success(result).to_json()


# 資金帳號
@bp.route('/funding', methods=['GET'])
@cross_origin()
def balance_funding():
    result = balance_service.get_funding_asset()
    logging.info(f'balance_funding: {json.dumps(result, indent=4, sort_keys=True)}')
    return { 
        "code": 0,
        "msg": "success",
        "data": result
    }

# 現貨帳號
@bp.route('/spot', methods=['GET'])
@cross_origin()
def spot_status():
    result = balance_service.get_spot_balance(asset='USDT')
    return { 
        "code": 0,
        "msg": "success",
        "data": [ result ]
    }
