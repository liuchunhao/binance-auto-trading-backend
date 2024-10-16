
# Binance Auto Trading Backend
A trading bot for Binance exchange, which is designed to trade cryptocurrencies. The bot is designed to be used with the Binance exchange. It is written in Python and uses the Binance API to interact with the exchange and provide API endpoints for the frontend.


## Table of Contents
- [Features](#features)
- [Quick Start](#quick-start)
    - [Configuration](#configuration)
    - [LINE Notify Management](#line-notify-management)
    - [API endpoints on Flask](#api-endpoints-on-flask)
    - [Real-time data server on Flask](#real-time-data-server-on-flask)
    - [Position check notify (every 30 seconds)](#position-check-notify-every-30-seconds)
    - [Funding fee notify (every 8 hours)](#funding-fee-notify-every-8-hours)
    - [Account status notify (once a day)](#account-status-notify-once-a-day)
    - [Stop all services](#stop-all-services)
    - [Run Redis on Docker](#run-redis-on-docker)
    - [SQLite](#sqlite)
    - [Run ngrok for LINE Webhook](#run-ngrok-for-line-webhook)
- [Deployment](#deployment)
- [Order Type Support](#order-type-support)
- [References](#references)


## Features
- [x] RESTful APIs for interacting with Binance & Exness exchange
  - [x] Order Management
  - [x] Wallet Management
  - [x] Position Management
  - [x] SMS push on mobile
- [x] WebSocket Server for Real-Time Data
  - [x] Market Data
  - [x] Account Update (Wallet, Position)
- [x] LINE Bot
  - [x] Daily PnL Report
  - [x] Funding Fee Notification
  - [x] Trading Signal Notification
- [x] Discord Bot
  - [x] Financial Report
  - [ ] ChatBot Integration with LLM
  - [ ] Configuration Management
  - [ ] Funding Fee Notification
  - [ ] Trading Signal Notification
- [x] Telegram Bot
  - [x] System Monitoring
- [x] Trading Bot for Binance Exchange
  - [ ] Auto Trading
 
---

## Quick Start

### Configuration
```ini
# src/.env

# Binace API
API_KEY = '******'
API_SECRET = '*********'

# Telegram Bot
TELEGRAM_TOKEN = '****************'

# LINE Bot
LINE_TOKEN = '**********************'
CHANNEL_ACCESS_TOKEN = '!@#$%^&*'
CHANNEL_SECRET = '123456789qwerasdfzxcv'

# Admin website Login
ADMIN_LOGIN_PASSWORD = 'p@$$w0rd'

# JWT token
JWT_SECRET = '@#$%^&*!'

# Discord bot token 
DISCORD_TOKEN = 'abc.efg.hijk'
DISCORD_WEBHOOK_NOTIFICATION = 'https://discord.com/api/webhooks/***********'
DISCORD_WEBHOOK_ANNOUNCEMENT = 'https://discord.com/api/webhooks/***********'
DISCORD_WEBHOOK_SECRET = 'https://discord.com/api/webhooks/*********'
DISCORD_WEBHOOK_WARNING = 'https://discord.com/api/webhooks/*********'

NUM_OF_UNITS = 9

# number of deposit unit
SIZE_OF_CONTRACTS = 9

# Initial deposit amount (USDT)
DEPOSIT = 9999

# SMS
SMS_APP_MOBILE_LIST = '+886*********,+886***********'
SMS_APP_MOBILE_HB_INTERVAL = 1800

```

### LINE Notify Management
- https://notify-bot.line.me/my


### API endpoints on Flask
```bash
sh/start_line_bot_server.sh
```

### Real-time data server on Flask
```bash
sh/start_ws_server_producer.sh
```

### Position check notify (every 30 seconds)
```bash
sh/futures_position_notify.sh
```

### Funding fee notify (every 8 hours)
```bash
sh/funding_fee_notify.sh
```

### Account status notify (once a day)
```bash
sh/futures_account_status_notify.sh
```

### Stop all services
```bash
sh/stop.sh
```

### Run Redis on Docker
```sh
cd docker/
docker-compose up -d
docker ps
```

### SQLite
```

```

### Run ngrok for LINE Webhook
```sh
/usr/bin/ngrok http 5000 --log=stdout &
```


## Deployment
```bash
# Start up all services
# 00 10 * * * ~/workspace/binance-line-bot/sh/start.sh

# Account report notify per day
# 00 8 * * * ~/workspace/binance-line-bot/sh/futures_account_status_notify.sh > ~/workspace/binance-line-bot/log/futures_account_status_notify.log 2>&1

# Funding fee notify per 8 hours
# 01  0 * * * /home/ubuntu/workspace/binance-line-bot/sh/funding_fee_notify.sh
# 01  8 * * * /home/ubuntu/workspace/binance-line-bot/sh/funding_fee_notify.sh
# 01 16 * * * /home/ubuntu/workspace/binance-line-bot/sh/funding_fee_notify.sh
30 07 * * * ~/workspace/binance-line-bot/sh/funding_fee_notify.sh

# Time sync (Not necessary on AWS)
# * * * * * /usr/bin/uptime > /tmp/uptime

# Clean log
# 0 0 * * 7 rm -f ~/workspace/binance-line-bot/nohup.out
0 0 10 * * rm -f ~/workspace/binance-line-bot/log/*
0 0 10 * * rm -f ~/workspace/react-examples/lege-management/nohup.out
0 0 10 * * rm -f ~/workspace/ngrok/nohup.out

# PnL update notify
* * * * * ~/workspace/binance-line-bot/sh/futures_position_notify.sh
```


## Order Type Support
- [x] Limit
- [x] Market
- [x] Post Only (只做Maker單)
- [x] Stop Limit (止損限價單)
- [x] Stop Market (止損市價單)
- [ ] Take Profit Limit (止盈限價單)
- [ ] Take Profit Market (止盈市價單)
- [ ] Trailing Stop Market (跟蹤止損單)
- [ ] Trailing Stop Limit (跟蹤限價單)
- [ ] Iceberg 
- [ ] TWAP (時間加權平均價)
- [ ] Scaled Orders (分批下單)


## References
- [雙向持倉模式下開倉與平倉](https://www.binance.com/zh-TC/support/faq/%E5%A6%82%E4%BD%95%E5%9C%A8%E9%9B%99%E5%90%91%E6%8C%81%E5%80%89%E6%A8%A1%E5%BC%8F%E4%B8%8B%E9%96%8B%E5%80%89%E8%88%87%E5%B9%B3%E5%80%89-360041515312) 
 
- Binance API
    * [Binance Error Code](https://binance-docs.github.io/apidocs/futures/en/#error-codes)
    * [Binance API](https://www.binance.com/en/binance-api)
    * [Binance Futures API](https://binance-docs.github.io/apidocs/futures/en/#new-order-trade)
    * [Binance API Management](https://www.binance.com/en/my/settings/api-management)
- Real-Time Data API
  * General Stream:
    - wss://stream.binance.com:9443/stream
  * Spot:
    - wss://stream.binance.com:9443/ws
  * Futures:
    - wss://fstream.binance.com:9443/ws
  * [Binance Websocket Samples](https://github.com/binance-exchange/python-binance/blob/master/binance/websockets.py)

- Python modules
  - [pbinance](https://pypi.org/project/pbinance/)
  - [binance-python](https://pypi.org/project/binance-python/)
    - [websockets](https://github.com/binance-exchange/python-binance/blob/master/binance/websockets.py)
    - [docs](https://python-binance.readthedocs.io/en/latest/binance.html#binance.websockets.BinanceSocketManager.isolated_margin_socket)

- Binance production real-time data API & URL：
    - Spot Price Websocket: 
        - wss://stream.binance.com:9443/ws
    - Spot Depth Websocket: 
        - wss://stream.binance.com:9443/ws/depth
    - Spot Kline/Candlestick Websocket: 
        - wss://stream.binance.com:9443/ws/kline
    - Spot Trade Websocket: 
        - wss://stream.binance.com:9443/ws/trade
    - Spot User Data Websocket: 
        - wss://stream.binance.com:9443/ws/userData
    - Spot Order Book (L2) Websocket: 
        - wss://stream.binance.com:9443/ws/dominance
    - Spot Order Book (L3) Websocket: 
        - wss://stream.binance.com:9443/ws/l3

    - Futures All Market Liquidation Order Websocket: 
        - wss://fstream.binance.com/ws
    - Futures Account Websocket: 
        - wss://fstream.binance.com/ws
    - Futures Mark Price Websocket: 
        - wss://fstream.binance.com/ws
    - Futures Kline/Candlestick Websocket: 
        - wss://fstream.binance.com/ws
    - Futures Continuous Contract Kline/Candlestick Websocket: 
        - wss://fstream.binance.com/ws
    - Futures Index Price Candlestick Websocket: 
        - wss://fstream.binance.com/ws
    - Futures Mark Price Kline/Candlestick Websocket: 
        - wss://fstream.binance.com/ws
    - Futures Order Book Depth Websocket: 
        - wss://fstream.binance.com/ws
    - Futures Ticker Websocket: 
        - wss://fstream.binance.com/ws
    - Futures Liquidation Order Websocket: 
        - wss://fstream.binance.com/ws
    - Futures Force Order Websocket: 
        - wss://fstream.binance.com/ws
    - Futures Premium Index Websocket: 
        - wss://fstream.binance.com/ws

    - Options Market Data Websocket: 
        - wss://fstream.binance.com/ws
    - Leveraged Tokens Websocket: 
        - wss://fstream.binance.com/ws

- Binance Spot Testnet URL
  - https://testnet.binance.vision/api
  - WebSocket API:
    - Spot: Spot, Margin(保證金交易), Isolated Margin(逐倉保證金交易) 
        - wss://testnet.binance.vision/ws
    - Futures: Binance Futures
        - wss://testnet.binance.vision/stream

- Wallet of Futures
    * Margin Balance = Wallet Balance + Unrealized PnL

- Websocket Streams
  - <symbol>@depth
  - <symbol>@depth@100ms
  - <symbol>@depth<levels>
  - <symbol>@depth<levels>@100ms
    > ex. btcusdt@depth10@100ms , push btc/usdt market data in depth 10 every 100ms


