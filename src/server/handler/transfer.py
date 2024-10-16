from service.binance.http import transfer_service
import json

# 4. 轉賬
def _transfer(command):
    '''
    ! transfer: from=spot, to=futures, amt=0.01
    ! transfer: from=futures, to=spot, amt=0.01
    ! transfer history: days=1
    '''
    reply_text = 'Not implemented yet'
    options = command.split(':')
    if len(options) >= 2:
        args = [ arg.strip() for arg in options[1].split(',') if arg != '' ]
        _from = ''
        _to = ''
        _amt = ''
        tranId = 0
        days = 0
        for arg in args:
            key_value = arg.split('=')
            if len(key_value) == 2:
                key = key_value[0]
                value = key_value[1]
                if key == 'from':
                    _from = value.upper()
                elif key == 'to':
                    _to = value.upper()
                elif key == 'amt':
                    _amt = value
                elif key == 'tranId':
                    tranId = value
                elif key == 'days':
                    days = int(value)

        type = options[0].split('transfer')[1].strip()
        result = ''
        if type == 'history':
            # 轉賬歷史紀錄
            reply_text = f'transfer {type}: tranId={_amt}, days={days}'
            if days != '':
                result = transfer_service.get_transfer_history_list(days=days)
            else:
                result = transfer_service.get_transfer_history_list(days=1)
        elif type == '':
            # 轉賬
            reply_text = f'transfer: from={_from}, to={_to}, amt={_amt}'
            if _from == 'SPOT' and _to == 'FUTURES':
                result = transfer_service.spot_transfer_to_futures(amount=_amt)
            elif _from == 'FUTURES' and _to == 'SPOT':
                result = transfer_service.futures_transfer_to_spot(amount=_amt)

        reply_text = f'{reply_text} -> result={json.dumps(result, indent=4, sort_keys=True)}'
    return reply_text