from common.utils import left_align

# help message
HELP_MESSAGE = left_align('''[指令清單]

重複上個命令: 
!!       

帳戶餘額查詢(現貨/合約/資金):
! balance spot  
! balance futures (DEPRECATED)
! balance funding (DEPRECATED)

部位查詢:
! position 

資金費率查詢:
! fee      

出金: (單位: USDT)
! withdraw: network=ETH, amt=1
! withdraw: network=TRX, amt=1

出金查詢:
! withdraw history
! withdraw code

入金地址查詢:
! deposit address: network=ETH
! deposit address: network=TRX

轉賬:
! transfer: from=spot, to=futures, amt=0.01
! transfer: from=futures, to=spot, amt=0.01

轉帳查詢:
! transfer history: days=1

合約下單: (數量單位: BTC)
- 限價單:
! order limit:  symbol=btcusdt, amt=0.001, side=sell, price=30000 
- 市價單:
! order market: symbol=btcusdt, amt=0.001, side=sell

合約刪單:
! order cancel: symbol=btcusdt, orderId=123456
! order cancel: symbol=btcusdt (取消全部)

合約平倉:
! order close: symbol=btcusdt

委託查詢:
! order status 
! order status: symbol=btcusdt
! order status: symbol=btcusdt, orderId=123456
''')

def get_help_message():
    return HELP_MESSAGE