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


import config

trading_client = TradingClient(config.api_key, config.secret_key, paper=True)
account = trading_client.get_account()

eth_ticker = yf.Ticker("ETH-USD")
eth_ticker = eth_ticker.history(period='50d')
eth_ticker = eth_ticker['Close']
posGains = 0
negGain = 0
pos = 0
neg = 0
x = 0

while(pos != 14 or neg != 14):
    if(eth_ticker[x] > eth_ticker[x+1] and (pos != 14)):
            posGains += eth_ticker[x]
            pos += 1
    elif(eth_ticker[x] < eth_ticker[x+1] and (neg != 14)):
            negGain += eth_ticker[x]
            neg += 1
    x += 1


gain14 = posGains/14
neg14 = negGain/14

rs = gain14 / neg14
rsi = (100)/(1+rs)
print(rsi)



if(rsi < 50):
        print("buying")
        market_order_data = MarketOrderRequest(
                        symbol="ETH/USD",
                        qty=1,
                        side=OrderSide.BUY,
                        time_in_force=TimeInForce.GTC
                        )
        # Market order
        market_order = trading_client.submit_order(
                        order_data=market_order_data
                        )
else:
        market_order_data = MarketOrderRequest(
                        symbol='ETH/USD',
                        qty=1,
                        side=OrderSide.SELL,
                        time_in_force=TimeInForce.GTC
                        )
        market_order = trading_client.submit_order(
                        order_data=market_order_data
                )