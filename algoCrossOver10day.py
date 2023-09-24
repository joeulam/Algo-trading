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
    pass_20_day = datetime.timedelta(days=20)
    pass_20_day = datetime.datetime.now() - pass_20_day 
    time_now = int(time_now.timestamp())
    pass_20_day = int(pass_20_day.timestamp())
    shortSMA = (finnhub_client.technical_indicator(symbol="AMD", 
                                            resolution='D', 
                                            _from=(pass_20_day), 
                                            to=(time_now), 
                                            indicator='SMA', 
                                            indicator_fields={"timeperiod": 10})
                                            )
    # Returns from old to new
    shortSMA = shortSMA['sma']
    shortSMALat = shortSMA[len(shortSMA)-index]
    # Gets latest shortSMA
    print("shortSMA: "+str(shortSMALat))
    return shortSMALat

def getLongSMA():
    time_now = datetime.datetime.now()
    pass_200_day = datetime.timedelta(days=200)
    pass_200_day = datetime.datetime.now() - pass_200_day
    time_now = int(time_now.timestamp())
    pass_200_day = int(pass_200_day.timestamp())

    longSMA = (finnhub_client.technical_indicator(symbol="AMD", 
                                            resolution='D', 
                                            _from=(pass_200_day), 
                                            to=(time_now), 
                                            indicator='SMA', 
                                            indicator_fields={"timeperiod": 50})
                                            )
    longSMA = longSMA['sma']
    longSMALat = longSMA[len(longSMA)-1]
    print("longSMA: "+str(longSMALat))
    return longSMALat

def get_Price():
    response = requests.get("https://data.alpaca.markets/v2/stocks/'AMD'/trades")
    data = response.json()
    print(data)
    amdP = data["trades"]["p"]
    return amdP





while(True):
  # SAVES API CALLS #
  shortSMALat = getShortSMA(1)
  LongSMA = getLongSMA()
  # Compares the SMA from the day before to see trend
  shortSMA = getShortSMA(2)


  if((shortSMALat == LongSMA) and shortSMA <= LongSMA):
      print("Buy at $" + str(shortSMALat))
      market_order_data = MarketOrderRequest(
                      symbol="AMD",
                      qty=1,
                      side=OrderSide.BUY,
                      time_in_force=TimeInForce.GTC
                      )
      # Market order
      market_order = trading_client.submit_order(
                      order_data=market_order_data
                  )

  elif((shortSMALat == LongSMA) and shortSMA >= LongSMA and (getStockQuant('AMD') >= 1)):
      print("Sell at $" + str(LongSMA))
      market_order_data = MarketOrderRequest(
          symbol='AMD',
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
          "longSMA: "+str(LongSMA)+ " at "+str(datetime.datetime.now())+'\n'
          "Ticket: AMD" + '\n'
          #"Current price: " +str(get_Price())
      )
  time.sleep(10)


"""while(True):
  url = "https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=USD"
  response = requests.get(url)
  data = response.json()
  eth_price_usd = data["USD"]
  if(eth_price_usd <= 1630.201):
    market_order_data = MarketOrderRequest(
                    symbol="ETH/USD",
                    qty=1.2,
                    side=OrderSide.BUY,
                    time_in_force=TimeInForce.GTC
                    )
    # Market order
    market_order = trading_client.submit_order(
                    order_data=market_order_data
                  )
  if(eth_price_usd >= 1673.718):
    # Sell a stock(Just change side to 'sell')
    market_order_data = MarketOrderRequest(
      symbol='ETH/USD',
      qty=1,
      side=OrderSide.SELL,
      time_in_force=TimeInForce.GTC
    )
    market_order = trading_client.submit_order(
                    order_data=market_order_data
                  )
  print("$"+ str(eth_price_usd) + " " + str(time.ctime(time.time())))
  time.sleep(1.5)
  """