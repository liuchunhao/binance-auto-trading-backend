from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
import json

from service.binance.http import deposit_service
from service.binance.http import withdraw_service
from service.binance.http import transfer_service

from model.r import R

bp = Blueprint('wallets_controller', __name__, url_prefix='/wallets')

############### Deposit ###################

# 入金錢包地址 (現貨)
@bp.route('/deposit/address', methods=['GET'])
@cross_origin()
def deposit_asset():
    params = request.args
    network = params.get('network')
    if network == None:
        network = 'TRX'
    result = deposit_service.get_deposit_address(network=network)
    return {
        "code": 0,
        "msg": "success",
        "data": result
    }

############### Withdrawal ###################

# 出金 (Sprt/Funding)
@bp.route('/withdraw', methods=['POST'])
@cross_origin()
def spot_withdraw():
    payload = request.get_json()
    # coin = payload['coin']            # USDT by default
    network = payload['network']        # TRX: TRC20, ETH: ERC20
    address = payload['address']        
    amount = payload['amount']          
    walletType = payload['walletType']  # 0: spot wallet,    1: funding wallet
    result = withdraw_service.withdraw(network=network, address=address, walletType=walletType, amount=amount)
    return { 
        "code": 0,
        "msg": "success",
        "data": result
    }

############## Transfer ####################

# 轉帳
@bp.route('/transfer', methods=['POST'])
@cross_origin()
def transfer_to():
    payload = request.get_json(force=True)  # force=True, above, is necessary if another developer forgot to set the MIME type to application/json
    asset = payload['asset']
    type = payload['type']          # 1: spot -> futures, 2: futures -> spot
    amount = payload['amount']
    result = transfer_service.transfer(asset=asset, type=type, amount=amount)
    return {
        "code": 0,
        "msg": "success",
        "data": result
    }


# 轉帳 (期貨 -> 現貨)
@bp.route('/transfer/futures', methods=['POST'])
@cross_origin()
def transfer_futures_to_spot():
    payload = request.get_json(force=True)  
    asset = payload['asset']
    amount = payload['amount']
    result = transfer_service.futures_transfer_to_spot(asset=asset, amount=amount)
    return { 
        "code": 0,
        "msg": "success",
        "data": result
    }

# 轉帳 (現貨 -> 期貨)
@bp.route('/transfer/spot', methods=['POST'])
@cross_origin()
def transfer_spot_to_futures():
    payload = request.get_json(force=True)
    asset = payload['asset']
    amount = payload['amount']
    result = transfer_service.spot_transfer_to_futures(asset=asset, amount=amount)
    return {
        "code": 0,
        "msg": "success",
        "data": result
    }


############## History ####################


# 出金查詢
@bp.route('/history/deposit', methods=['GET'])
@cross_origin()
def deposit_history():
    result = deposit_service.get_deposit_history()
    return R.success(result)

# 轉帳查詢
@bp.route('/history/transfer', methods=['GET'])
@cross_origin()
def transfer_history():
    result = transfer_service.get_transfer_history_list()
    return R.success(result)

# 入金查入
@bp.route('/history/withdraw', methods=['GET'])
@cross_origin()
def withdraw_history():
    result = withdraw_service.get_withdraw_history()
    return R.success(result)
    

##################################


# 出金狀態碼
@bp.route('/withdraw/status-code', methods=['GET'])
@cross_origin()
def withdraw_status_code():
    result = withdraw_service.get_withdraw_status_code()
    return { 
        "code": 0,
        "msg": "success",
        "data": result
    }
