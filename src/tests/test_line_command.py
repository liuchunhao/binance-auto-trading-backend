# Desc: Test the line command

# Usage: python -m unittest tests.test_line_command
import sys
sys.path.append('src')

from server import linebot_server
from common.utils import left_align

if __name__ == '__main__':
    # command = bot_server.parse_command('! help')
    # bot_server.dispatch(command)

    commands = '''
    #! withdraw: network=ETH, amt=5
    ! withdraw: network=TRX, amt=5
    #! withdraw history
    #! withdraw code
    #! deposit address: network=ETH
    #! deposit address: network=TRX
    #! transfer: from=spot, to=futures, amt=5
    #! transfer: from=futures, to=spot, amt=5
    #! transfer history: days=1
    #! order limit:  symbol=btcusdt, amt=0.001, side=sell, price=32000 
    #! order market: symbol=btcusdt, amt=0.001, side=sell
    #! order cancel: symbol=btcusdt, orderId=184865060477
    #! order close: symbol=btcusdt
    #! order status 
    #! order status: symbol=btcusdt
    #! order status: symbol=btcusdt, orderId=184903685164
    #! order status: symbol=btcusdt, orderId=184865060477
    #! balance spot
    #! balance futures
    #! balance funding
    #! position
    '''

    for command in [ command for command in commands.split('\n') if not command.startswith('#') ]:
        command = left_align(command)
        command = linebot_server.parse_command(command)
        linebot_server.dispatch(command)
        print()
