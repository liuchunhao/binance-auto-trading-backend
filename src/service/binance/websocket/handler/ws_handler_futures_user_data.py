import json
import logging

from common.utils import left_align
from common.datetime import epoch_to_date, render_epoch_time


def log_decorator(func):
    def wrapper(*args, **kwargs):
        logging.info(f'Entering: {func.__name__}')
        logging.info(f'Arguments: {args}, {kwargs}')
        result = func(*args, **kwargs)
        logging.info(f'Exiting: {func.__name__}')
        return result
    return wrapper


# ACCOUNT_UPDATE
@log_decorator
def account_update(msg):
    
    '''
    - https://binance-docs.github.io/apidocs/futures/en/#event-balance-and-position-update

    - payload:

        {
            "e": "ACCOUNT_UPDATE",
            "E": 1682870400991,                     # event time
            "T": 1682870400987,                     # transaction time
            "a": {                                  # account update
                "m": "FUNDING_FEE",                 # event reason type:  WITHDRAW / DEPOSIT (出金/入金) / FUNDING_FEE (資金費率) / ADJUSTMENT (調整) / AUTO_REPAY (自動還款) / MARGIN_TRANSFER (保證金轉移) / MARGIN_TYPE_CHANGE (保證金類型變更) / ASSET_TRANSFER (資產轉移) / EXTERNAL_TRANSFER (外部轉移)
                "B": [                              # balance
                    {
                        "a": "USDT",                # asset
                        "bc": "7.20795369",         # balance change except for PnL and commission.
                        "cw": "50091.69717692",     # crossWalletBalance
                        "wb": "50091.69717692"      # walletBalance
                    }
                ],
                "P": [
                    {
                        "s":"BTCUSDT",            // Symbol
                        "pa":"0",                 // Position Amount
                        "ep":"0.00000",           // Entry Price
                        "bep":"0",                // breakeven price
                        "cr":"200",               // (Pre-fee) Accumulated Realized
                        "up":"0",                 // Unrealized PnL
                        "mt":"isolated",          // Margin Type
                        "iw":"0.00000000",        // Isolated Wallet (if isolated position)
                        "ps":"BOTH"               // Position Side
                    }，
                ]                                
            }
        }
    '''
    res = {
        'eventType': msg['e'],
        'eventTime': render_epoch_time((msg['E'])),
        'transactionTime': render_epoch_time(msg['T']),
        'accountUpdate': {
            'eventReason': msg['a']['m'],
            'balances': [ { 
                            'asset': b['a'], 
                            'walletBalance': b['wb'], 
                            'crossWalletBalance': b['cw'], 
                            'balanceChange': b['bc'] 
                        } for b in msg['a']['B'] 
                        ],
            'positions': [ { 
                            'symbol': p['s'], 
                            'positionAmt': p['pa'], 
                            'entryPrice': p['ep'], 
                            'breakevenPrice': p['bep'], 
                            'accumulatedRealized': p['cr'], 
                            'unrealizedPnL': p['up'], 
                            'marginType': p['mt'], 
                            'isolatedWallet': p['iw'], 
                            'positionSide': p['ps'] 
                            } for p in msg['a']['P'] 
                        ]
        }
    }
    return json.dumps(res, indent=4, sort_keys=True)


# MARGIN_CALL
@log_decorator
def margin_call(msg):
    '''
    - https://binance-docs.github.io/apidocs/futures/en/#event-margin-call
    - payload:
        {
            "e":"MARGIN_CALL",      // Event Type
            "E":1587727187525,      // Event Time
            "cw":"3.16812045",      // Cross Wallet Balance. Only pushed with crossed position margin call
            "p":[                   // Position(s) of Margin Call
            {
                "s":"ETHUSDT",      // Symbol
                "ps":"LONG",        // Position Side
                "pa":"1.327",       // Position Amount
                "mt":"CROSSED",     // Margin Type
                "iw":"0",           // Isolated Wallet (if isolated position)
                "mp":"187.17127",   // Mark Price
                "up":"-1.166074",   // Unrealized PnL
                "mm":"1.614445"     // Maintenance Margin Required
            }
            ]
        }  
    '''
    res = {
        'eventType': msg['e'],
        'eventTime': render_epoch_time(msg['E']),
        'crossWalletBalance': msg['cw'],
        'positions': [ {
                        'symbol': p['s'],
                        'positionSide': p['ps'],
                        'positionAmt': p['pa'],
                        'marginType': p['mt'],
                        'isolatedWallet': p['iw'],
                        'markPrice': p['mp'],
                        'unrealizedPnL': p['up'],
                        'maintenanceMarginRequired': p['mm']
                        } for p in msg['p']
                    ]
    }
    return json.dumps(res, indent=4, sort_keys=True)


# ORDER_TRADE_UPDATE
@log_decorator
def order_trade_update(msg):
    '''
    - https://binance-docs.github.io/apidocs/futures/en/#event-order-update

    - payload:

        {
            "e":"ORDER_TRADE_UPDATE",       // Event Type
            "E":1568879465651,              // Event Time
            "T":1568879465650,              // Transaction Time
            "o":{                             
                "s":"BTCUSDT",              // Symbol
                "c":"TEST",                 // Client Order Id
                                            // special client order id:
                                            // starts with "autoclose-": liquidation order
                                            // "adl_autoclose": ADL auto close order
                                            // "settlement_autoclose-": settlement order for delisting or delivery
                "S":"SELL",                 // Side
                "o":"TRAILING_STOP_MARKET", // Order Type
                "f":"GTC",                  // Time in Force
                "q":"0.001",                // Original Quantity
                "p":"0",                    // Original Price
                "ap":"0",                   // Average Price
                "sp":"7103.04",             // Stop Price. Please ignore with TRAILING_STOP_MARKET order
                "x":"NEW",                  // Execution Type
                "X":"NEW",                  // Order Status
                "i":8886774,                // Order Id
                "l":"0",                    // Order Last Filled Quantity
                "z":"0",                    // Order Filled Accumulated Quantity
                "L":"0",                    // Last Filled Price
                "N":"USDT",                 // Commission Asset, will not push if no commission
                "n":"0",                    // Commission, will not push if no commission
                "T":1568879465650,          // Order Trade Time
                "t":0,                      // Trade Id
                "b":"0",                    // Bids Notional
                "a":"9.91",                 // Ask Notional
                "m":false,                  // Is this trade the maker side?
                "R":false,                  // Is this reduce only
                "wt":"CONTRACT_PRICE",      // Stop Price Working Type
                "ot":"TRAILING_STOP_MARKET",// Original Order Type
                "ps":"LONG",                // Position Side
                "cp":false,                 // If Close-All, pushed with conditional order
                "ap":"7476.89",             // Activation Price, only puhed with TRAILING_STOP_MARKET order
                "cr":"5.0",                 // Callback Rate, only puhed with TRAILING_STOP_MARKET order
                "pP": false,                // If price protection is turned on
                "si": 0,                    // ignore
                "ss": 0,                    // ignore
                "rp":"0",                   // Realized Profit of the trade
                "V":"EXPIRE_TAKER",         // STP mode
                "pm":"OPPONENT",            // Price match mode
                "gtd":0                     // TIF GTD order auto cancel time
            }
        }
    '''

    res = {
        'eventType': msg['e'],
        'eventTime': render_epoch_time(msg['E']),
        'transactionTime': render_epoch_time(msg['T']),
        'orderUpdate': {
            'symbol': msg['o']['s'],
            'clientOrderId': msg['o']['c'],
            'side': msg['o']['S'],
            'orderType': msg['o']['o'],
            'timeInForce': msg['o']['f'],
            'quantity': msg['o']['q'],
            'price': msg['o']['p'],
            'averagePrice': msg['o']['ap'],
            'stopPrice': msg['o']['sp'],
            'executionType': msg['o']['x'],
            'orderStatus': msg['o']['X'],
            'orderId': msg['o']['i'],
            'orderLastFilledQuantity': msg['o']['l'],
            'orderFilledAccumulatedQuantity': msg['o']['z'],
            'lastFilledPrice': msg['o']['L'],
            'commissionAsset': msg['o']['N'],
            'commission': msg['o']['n'],
            'orderTradeTime': msg['o']['T'],
            'tradeId': msg['o']['t'],
            'bidsNotional': msg['o']['b'],
            'askNotional': msg['o']['a'],
            'isMakerSide': msg['o']['m'],
            'isReduceOnly': msg['o']['R'],
            'stopPriceWorkingType': msg['o']['wt'],
            'originalOrderType': msg['o']['ot'],
            'positionSide': msg['o']['ps'],
            'isCloseAll': msg['o']['cp'],
            # 'activationPrice': msg['o']['AP'],   # only puhed with TRAILING_STOP_MARKET order
            # 'callbackRate': msg['o']['cr'],      # only puhed with TRAILING_STOP_MARKET order
            'priceProtection': msg['o']['pP'],
            'realizedProfit': msg['o']['rp'],
            'stpMode': msg['o']['V'],
            'priceMatchMode': msg['o']['pm'],
            'tifGtdOrderAutoCancelTime': msg['o']['gtd']
        }
    }
    return json.dumps(res, indent=4, sort_keys=True)


class FuturesUserDataHandler():

    def __init__(self, callback) -> None:
        self.callback = callback

    def handle(self, msg): 
        logging.info(f"handle_futures_user_socket: {json.dumps(msg, indent=4, sort_keys=True)}")
        res = None
        event_type = msg['e']
        if event_type == 'ACCOUNT_UPDATE':
            res = account_update(msg)

            '''
            account_update = msg['a']
            event_reason_type = account_update['m'] 
            if event_reason_type == 'FUNDING_FEE':
                result = f"""
                [合約帳戶異動]
                原因: 資金費率
                資產: {account_update['B'][0]['a']}
                餘額異動: {account_update['B'][0]['bc']}
                錢包餘額: {account_update['B'][0]['wb']}
                """
            elif event_reason_type == 'WITHDRAW':
                result = f"""
                [合約帳戶異動]
                原因: 帳戶出金
                資產: {account_update['B'][0]['a']}
                餘額異動: {account_update['B'][0]['bc']}
                錢包餘額: {account_update['B'][0]['wb']}
                """
            elif event_reason_type == 'DEPOSIT':
                result = f"""
                [合約帳戶異動]
                原因: 帳戶入金
                資產: {account_update['B'][0]['a']}
                餘額異動: {account_update['B'][0]['bc']}
                錢包餘額: {account_update['B'][0]['wb']}
                """
            elif event_reason_type == 'MARGIN_CALL':
                result = f"""
                [合約帳戶異動]
                原因: 保證金不足
                資產: {account_update['B'][0]['a']}
                餘額異動: {account_update['B'][0]['bc']}
                錢包餘額: {account_update['B'][0]['wb']}
                """
            '''

        elif event_type == 'ORDER_TRADE_UPDATE':
            res = order_trade_update(msg)

            '''
            order = msg['o']
            result = f"""
            [合約交易狀態異動]
            合約: {order['s']}
            Side: {order['S']}
            價格: {order['p']}
            數量(BTC): {order['q']}
            委託類別: {order['o']}
            訂單狀態: {order['X']}
            訂單ID: {order['i']}
            更新時間: {epoch_to_date(order['T'])}
            下單裝置: {order['c']}
            """
            '''
        elif event_type == 'ACCOUNT_CONFIG_UPDATE':
            pass
        elif event_type == 'ACCOUNT_UPDATE':
            res = margin_call(msg)
        elif event_type == 'error':
            '''
                {
                    "e": "error",
                    "m": "Max reconnect retries reached"
                }
            '''
        else:
            res = f"handle_futures_user_socket|unknown event: {event_type}"

        logging.info(f"handle_futures_user_socket|result: {json.dumps(res, indent=4, sort_keys=True)}")

        self.callback(res)
        