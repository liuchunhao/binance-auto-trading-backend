
class Payload:
    EVENT_TYPE = 'e'
    EVENT_TIME = 'E'
    SYMBOL = 's'
    PRICE_CHANGE = 'P'
    PRICE_CHANGE_PERCENT = 'P'

    open_price = 'o'
    high_price = 'h'
    low_price = 'l'
    last_price = 'c'
    weighted_avg_price = 'w'
    total_traded_base_asset_volume = 'v'
    total_traded_quote_asset_volume = 'q'
    statistics_open_time = 'O'
    statistics_close_time = 'C'
    first_trade_id = 'F'
    last_trade_id = 'L'
    total_number_of_trades = 'n'

    best_bid_price = 'b'
    best_bid_quantity = 'B'
    best_ask_price = 'a'
    best_ask_quantity = 'A'
    order_book_updateId = 'u'

    prev_close_price = 'x'

    average_px = 'ap'

class AccountUpdate:
    Event_TYPE = 'e'
    EVENT_TIME = 'E'
    TRANSACTION_TIME = 'T'
    
    UPDATE_DATA = 'a'
    EVENT_REASON_TYPE = 'm' # FUNDING_FEE, 

    BALANCE_UPDATE = 'B'
    ASSET = 'a'
    WALLET_BALANCE = 'wb'
    CROSS_WALLET_BALANCE = 'cw'
    BALANCE_CHANGE_EXCEPT_PnL_AND_COMMISSION = 'bc'

    POSITION_UPDATE = 'P'
    SYMBOL = 's'
    POSITION_AMOUNT = 'pa'
    ENTRY_PRICE = 'ep'
    PREMIUM_FEE_ACCUMULATED_REALIZED = 'cr'
    UNREALIZED_PnL = 'up'
    POSITION_MARGIN_TYPE = 'mt'
    ISOLATED_WALLET = 'iw'
    POSITION_SIDE = 'ps'


    '''
    https://binance-docs.github.io/apidocs/spot/en/#all-market-tickers-stream


    - futures_user_socket
    message type: {
        "E": 1682812802637,
        "T": 1682812802634,
        "a": {
            "B": [
                {
                    "a": "USDT",
                    "bc": "11.94066535",
                    "cw": "50080.39277316",
                    "wb": "50080.39277316"
                }
            ],
            "P": [],
            "m": "FUNDING_FEE"
        },
        "e": "ACCOUNT_UPDATE"
    }

   
    - bookTicker: 
    message type: {
       "data": {
           "A": "10.20100000",
           "B": "7.23700000",
           "a": "0.01103800",
           "b": "0.01103700",
           "s": "BNBBTC",
           "u": 3043016670
       },
       "stream": "bnbbtc@bookTicker"
   }

   - miniTicker = 24hrMiniTicker:

   - ticker = 24hrTicker
   message type: {
        "data": {
            "A": "5.07053000",
            "B": "6.94130000",
            "C": 1682744051019,
            "E": 1682744051019,
            "F": 3098730432,
            "L": 3099795858,
            "O": 1682657651019,
            "P": "-0.386",
            "Q": "0.01800000",
            "a": "29366.81000000",
            "b": "29366.80000000",
            "c": "29366.81000000",
            "e": "24hrTicker",
            "h": "29566.92000000",
            "l": "28891.00000000",
            "n": 1065427,
            "o": "29480.70000000",
            "p": "-113.89000000",
            "q": "1434208493.98028060",
            "s": "BTCUSDT",
            "v": "49008.26228000",
            "w": "29264.62656003",
            "x": "29480.70000000"
        },
        "stream": "btcusdt@ticker"
    }

    A: 最佳買方的委託數量
    B: 最佳賣方的委託數量
    C: 統計結束時間戳
    E: 事件時間戳
    F: 統計期間內第一筆成交ID
    L: 統計期間內最後一筆成交ID
    O: 統計開始時間戳
    P: 24小時價格變化百分比
    Q: 24小時成交量（基幣）
    a: 最佳賣方的委託價格
    b: 最佳買方的委託價格
    c: 最新成交價格
    e: 事件類型
    h: 24小時最高價
    l: 24小時最低價
    n: 24小時成交筆數
    o: 24小時開盤價
    p: 24小時價格變化
    q: 24小時成交量（報價幣）
    s: 交易對
    u: 更新ID
    v: 24小時成交量（計價幣）
    w: 24小時加權平均價
    x: 統計開始時的最新成交價格
    stream: 數據流名稱

   '''
