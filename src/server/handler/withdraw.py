from service.binance.http import withdraw_service
import json

# 3. 出金
def _withdraw(command):
    '''
    ! withdraw: network=ETH, amt=0.01
    ! withdraw: network=TRX, amt=0.01
    ! withdraw history
    ! withdraw code
    '''
    reply_text = 'Not implemented yet'
    result = ''
    options = command.split(':') 
    if len(options) >= 2:
        args = [ arg.strip() for arg in options[1].split(',') if arg != '' ]
        network = ''
        amt = 0.0
        for arg in args:
            key_value = arg.split('=')
            if len(key_value) == 2:
                key = key_value[0]
                value = key_value[1]
                if key == 'network':
                    network = value.upper()
                elif key == 'amt':
                    amt = value
        reply_text = f'withdraw: network={network}, amt={amt}'
        result = withdraw_service.withdraw(network=network, amount=amt)
    elif len(options) == 1:
        type = options[0].split('withdraw')[1].strip()
        reply_text = f'withdraw {type}'
        if type == 'history':
            # 出金歷史紀錄
            reply_text = f'withdraw {type}'
            result = withdraw_service.get_withdraw_history()
        elif type == 'code':
            result = withdraw_service.get_withdraw_status_code()
        else:
            reply_text = 'Unknown command: withdraw {type}'
    reply_text = f'{reply_text} -> result={json.dumps(result, indent=4, sort_keys=True)}'
    return reply_text
    