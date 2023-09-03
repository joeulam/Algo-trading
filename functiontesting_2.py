import asyncio
import alpaca_trade_api as tradeapi
from alpaca_trade_api.stream import Stream
from alpaca_trade_api.common import URL
import requests
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.trading.client import TradingClient
import alpaca_trade_api as tradeapi
from alpaca_trade_api.rest import REST, TimeFrame, TimeFrameUnit
import json
import time
import finnhub
from alpaca.data.live import StockDataStream
import yfinance as yf
import pandas as pd
import datetime 
import logging
import logging.handlers


import config
import ssl
import websocket


import ssl
import websocket

def on_message(ws, message):
    data = json.loads(message)
    if 'price' in data:
        price = data['price']
        print("Price:", price)

ws = websocket.WebSocketApp(
    "wss://api.gemini.com/v1/marketdata/ETHUSD",
    on_message=on_message)
ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})