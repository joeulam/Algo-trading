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
# preparing orders

def get_Long():
    eth_ticker = yf.Ticker("ETH-USD")
    eth_ticker = eth_ticker.history(period='10d')
    price = 0 
    eth_ticker = eth_ticker['Close']
    for i, x in enumerate (eth_ticker):
        price += x
    Sma30Day = price/len(eth_ticker)
    return Sma30Day
    print("Long SMA:"+str(Sma30Day))

def get_Short():
    eth_ticker = yf.Ticker("ETH-USD")
    eth_ticker = eth_ticker.history(period='5m')
    price = 0 
    eth_ticker = eth_ticker['Close']
    for i, x in enumerate (eth_ticker):
        price += x
    Sma1Day = price/len(eth_ticker)
    return Sma1Day
    print("Short SMA:"+str(Sma1Day))

def get_price():
    eth_ticker = yf.Ticker("ETH-USD")
    eth_ticker = eth_ticker.history(period='5m')
    price = 0 
    eth_ticker = eth_ticker['Close']
    for i, x in enumerate (eth_ticker):
        price += x
    return price

def getStockQuant(symbol):
    stock_quant = trading_client.get_open_position(symbol)
    return stock_quant.qty

while(True):
    Sma1Day = get_Short()
    Sma30Day = get_Long()
    price = get_price()
    url = "https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=USD"
    response = requests.get(url)
    data = response.json()
    eth_price_usd = data["USD"]
    if((Sma1Day == Sma30Day) and (Sma1Day < ((price - eth_ticker[len(eth_ticker)-1])/len(eth_ticker))) or (eth_price_usd < 1600) ):
        print("buy")
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
    elif((Sma1Day == Sma30Day) and (Sma1Day > ((price - eth_ticker[len(eth_ticker)-1])/len(eth_ticker))) and getStockQuant('ETH') >= 1):
        print('sell')
        market_order_data = MarketOrderRequest(
                    symbol='ETH/USD',
                    qty=1,
                    side=OrderSide.SELL,
                    time_in_force=TimeInForce.GTC
                    )
        market_order = trading_client.submit_order(
                        order_data=market_order_data
                    )
    else:
        print('\n'+"------------------ \n"+'Current SMA: \n'+
            "shortSMA: "+str(Sma1Day) + " at "+str(datetime.datetime.now())+'\n'
            "longSMA: "+str(Sma30Day)+ " at "+str(datetime.datetime.now())+'\n'
            "Current Price is: $"+str(eth_price_usd)
        )
    time.sleep(5)
