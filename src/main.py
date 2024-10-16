from server import linebot_server
from service.binance import user_data
from common.utils import *
from common.database import *

from service.binance.user_data import *
from service.binance.http import *

import textwrap
from controller import linebot_webhook_controller

def test_parse_mt5_command():
    text = '''
    【MT5】
    8點定時回報 
    預付款:4827.00, 淨值:28308.40, 預付款比例:597.25%'''
    print(text)
    text = textwrap.dedent(text)
    command = linebot_webhook_controller.parse_command(text)
    print(f'command: {command}')

    
if __name__ == '__main__':
    # bot_server.app.run()

    # 資金費率
    # user_data.get_funding_fee_history('BNBUSDT')
    # binance_data.run()

    # 合約帳號資訊
    user_data.get_futures_account_status()
    # user_data.get_price_history('BNBUSDT')

    # 最新標記價格
    # time, markPrice = user_data.get_latest_mark_price('BNBUSDT')
    # user_data.get_latest_mark_price('BTCUSDT')
    # print(f'time: {time}, markPrice: {markPrice}')

    # 解析MT5帳號資訊
    # margin, totalBalance = user_data.parse_mt5_account_status()
    # print(f'margin: {margin}, totalBalance: {totalBalance}')

    # MT5帳號資訊
    # margin, totalBalance = user_data.get_mt5_account_status()
    # print(f'margin: {margin}, totalBalance: {totalBalance}')
    # insert_mt5_balance(margin=margin, balance=totalBalance)

    # 昨日資金費率
    # get_yesterday_funding_fee_sum('BTCUSDT')

    # 美元匯率
    # logging.info(f'{get_exchange_rate("USDT", "TWD")}')

    # 查詢轉帳歷史紀錄
    # user_data.get_futures_balance()   # deprecated!
    
    # 現貨帳戶餘額
    # balance.get_spot_balance()
    # balance.get_account_balance()
    
    # 資金帳戶餘額
    
    # 2. websocket 帳戶餘額是否有異動 
    # 2.1 現貨帳戶餘額是否有異動 （立刻轉帳到合約帳戶）

    # 2.2 合約帳戶餘額是否有異動 

    # 2.3 資金帳戶餘額是否有異動
    
    # 2.4 任何資金流動都要通知 (轉帳、出入金、交易)
    

    # 3. 儲值錢包地址
    # import websocket.deposit as deposit
    # deposit.get_deposit_address(network='TRX')
    # deposit.get_deposit_address(network='ETH')

    # 4. 出金
    # tranId = user_data.withdraw(amount=1, walletType=0)


    # 4.1 出金狀態查詢
    # tranId = 'a337d8806fae48e9a273c26b9f610fd8'
    # user_data.get_withdraw_history()


    # 5 入金查詢
    # user_data.get_deposit_history() 


    # 6 合約 (futures)
    # 6.1 下單 (數量要用BTC計算)
    # orderId = user_data.futures_create_limit_order(symbol='BTCUSDT', side='SELL', quantity=0.001, price=30000)
    

    # 6.1.1 查詢BTC價格 換算成USDT

     
    # 6.3 取消
    # symbol = 'BTCUSDT'
    # orderId = 184325414868
    # user_data.futures_cancel_order(symbol=symbol, orderId=orderId)

    # 6.2 平倉
    
    # 6.2 查詢委託狀態(是否成交)
    # futures_get_all_open_orders()
    # futures_get_open_orders(symbol='BTCUSDT')

    # 6.3 查詢歷史委託
    # futures_get_order_by_orderId(symbol='BTCUSDT', orderId=orderId)

    # 6.4 查詢成交歷史
    # https://binance-docs.github.io/apidocs/futures/cn/#v2-user_data-3


    # 6.5 手續費率

    # --------------------------------------------------    

    # 7 websocket 訂閱合約狀態
    # 7.1 最新合約價格


    # 7.2 Margin Call
    # https://binance-docs.github.io/apidocs/futures/cn/#websocket-3

    
    # 7.3 訂單/交易更新
    
    
    # 8 帳戶設定更新通知
    # 8.1 約定出金地址異動通知


    # user_data.get_order_book('BTCUSDT')
    # user_data.get_latest_price('BTCUSDT')
    # user_data.get_latest_mark_price('BTCUSDT')
    

    # 匯率
    # import data.currency as data
    # result = data.get_currency_rate('USD', 'TWD')
    # logging.info(f'result: {result}'.ljust(0))
    # get_exchange_rate('USD', 'TWD')
    