from service.binance.http import deposit_service
import json

# 2. 入金
def _deposit(command):
    '''
    入金地址查詢:
    ! deposit address: network=ETH
    ! deposit address: network=TRX
    '''
    reply_text = 'Not implemented yet'
    result = ''
    options = command.split(':')
    if len(options) >= 2:
        args = [ arg.strip() for arg in options[1].split(',') if arg != '' ]
        network = ''
        amt = ''
        for arg in args:
            key_value = arg.split('=')
            if len(key_value) == 2:
                key = key_value[0]
                value = key_value[1]
                if key == 'network':
                    network = value.upper()
                elif key == 'amt':
                    amt = value
        type = options[0].split('deposit')[1].strip()
        if type == 'address': 
            # 入金地址查詢
            reply_text = f'deposit {type}: network={network}'
            result = deposit_service.get_deposit_address(network)
        elif type == '':
            # 入金
            reply_text = f'deposit {type}: network={network}, amt={amt}'
        else:
            reply_text = f'Unknown command: deposit {type}'
    reply_text = f'{reply_text} -> result={json.dumps(result, indent=4, sort_keys=True)}'        
    return reply_text
