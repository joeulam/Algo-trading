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
import datetime 
import websocket

# ALL API SETUP 
# Alpaca
api_key = 'PK1XBVTFYABBZA2IP8LR'
secret_key = 'drrhgQOS7ffpAawfrMndih83O8FSHgfn1eOEjIUc'
trading_client = TradingClient(api_key, secret_key, paper=True)
account = trading_client.get_account()

# Fin hub
api_key_fin = 'cjkfenpr01quh8qr835gcjkfenpr01quh8qr8360'
finnhub_client = finnhub.Client(api_key=api_key_fin)

# Variable setup


def getStockQuant(symbol):
    stock_quant = trading_client.get_open_position(symbol)
    return stock_quant.qty


def getShortSMA(index):
    time_now = datetime.datetime.now()
    pass_20_day = datetime.timedelta(days=6)
    pass_20_day = datetime.datetime.now() - pass_20_day 
    time_now = int(time_now.timestamp())
    pass_20_day = int(pass_20_day.timestamp())
    shortSMA = (finnhub_client.technical_indicator(symbol="TSLA", 
                                            resolution='30', 
                                            _from=(pass_20_day), 
                                            to=(time_now), 
                                            indicator='SMA', 
                                            indicator_fields={"timeperiod": 5})
                                            )
    # Returns from old to new
    shortSMA = shortSMA['sma']
    shortSMALat = shortSMA[len(shortSMA)-index]
    # Gets latest shortSMA
    return shortSMALat
    print("shortSMA: "+str(shortSMALat) + " at "+str(datetime.datetime.now()))


def getLongSMA():
    time_now = datetime.datetime.now()
    pass_200_day = datetime.timedelta(days=10)
    pass_200_day = datetime.datetime.now() - pass_200_day
    time_now = int(time_now.timestamp())
    pass_200_day = int(pass_200_day.timestamp())

    longSMA = (finnhub_client.technical_indicator(symbol="TSLA", 
                                            resolution='60', 
                                            _from=(pass_200_day), 
                                            to=(time_now), 
                                            indicator='SMA', 
                                            indicator_fields={"timeperiod": 30})
                                            )
    longSMA = longSMA['sma']
    longSMALat = longSMA[len(longSMA)-1]
    return longSMALat
    print("longSMA: "+str(longSMALat)+ " at "+str(datetime.datetime.now()))

    
while(True):
    # SAVES API CALLS #
    shortSMALat = getShortSMA(1)
    LongSMA = getLongSMA()
    # Compares the SMA from the day before to see trend
    shortSMA = getShortSMA(2)


    if((shortSMALat == LongSMA) and shortSMA <= LongSMA):
        print("Buy at $" + str(shortSMALat))
        market_order_data = MarketOrderRequest(
                        symbol="TSLA",
                        qty=1,
                        side=OrderSide.BUY,
                        time_in_force=TimeInForce.GTC
                        )
        # Market order
        market_order = trading_client.submit_order(
                        order_data=market_order_data
                    )

    elif((shortSMALat == LongSMA) and shortSMA >= LongSMA and (getStockQuant('TSLA') >= 1)):
        print("Sell at $" + str(LongSMA))
        market_order_data = MarketOrderRequest(
            symbol='TSLA',
            qty=1,
            side=OrderSide.SELL,
            time_in_force=TimeInForce.GTC
            )
        market_order = trading_client.submit_order(
                            order_data=market_order_data
                        )
    else:
        print('\n'+"------------------ \n"+'Current SMA: \n'+
            "shortSMA: "+str(shortSMALat) + " at "+str(datetime.datetime.now())+'\n'
            "longSMA: "+str(LongSMA)+ " at "+str(datetime.datetime.now())
        )
    time.sleep(10)
