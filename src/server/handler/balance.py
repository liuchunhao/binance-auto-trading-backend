import json

from service.binance.http import balance_service
from service.binance import user_data

# 5. 餘額查詢
def _balance(command):
    '''
    ! balance spot  
    ! balance futures (DEPRECATED)
    ! balance funding (DEPRECATED)
    '''
    option = command.split('balance')[1].strip()
    if option == 'spot':
        # 現貨帳戶餘額
        reply_text = f'{json.dumps(balance_service.get_spot_balance(), indent=4, sort_keys=True)}'
    elif option == 'futures':
        # 合約帳戶餘額
        total_margin_balance, margin, reply_text = user_data.get_futures_account_status()
    elif option == 'funding':
        # 資金帳戶餘額
        reply_text = balance_service.get_funding_asset()
    else:
        reply_text = f'Unknown command: balance {option}'
    return reply_text
       