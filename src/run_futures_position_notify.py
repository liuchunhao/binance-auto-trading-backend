from service.binance import user_data
from service.linebot.notification import send_line_notify

if __name__ == '__main__':
    # res = user_data.futures_account_status()
    time, positionAmt, totalMarginBalance, btc_mark_price, margin_call, leverage = user_data.position_leverage_status()
    print(time)
    print(positionAmt)
    print(totalMarginBalance)
    print(btc_mark_price)
    print(margin_call)
    print(leverage)
    msg = '''
    Update time: {time}
    Position amount: {positionAmt}
    Margin balance: {totalMarginBalance}
    BTC market price: {btc_mark_price}
    Margin call: {margin_call}
    Leverage: {leverage}
    '''.format(time=time, positionAmt=positionAmt, totalMarginBalance=totalMarginBalance, btc_mark_price=btc_mark_price, margin_call=margin_call, leverage=leverage)

    msg = '\n'.join([line.lstrip() for line in msg.split('\n')])

    limit = 15
    if leverage >= limit:
        msg = f'''️️\n{msg}
        槓桿超過{limit}倍，請注意幣安風險！
        '''.format(limit=limit)

        msg = '\n'.join([line.lstrip() for line in msg.split('\n')])
        send_line_notify(msg)

    
    # limit = 6
    limit = 0.1
    if leverage <= limit:
        msg = f'''️️\n{msg}
        槓桿低於{limit}倍，請注意Exness風險！
        '''.format(limit=limit)

        msg = '\n'.join([line.lstrip() for line in msg.split('\n')])
        send_line_notify(msg)

    print(msg)

