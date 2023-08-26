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

api_key = 'PK1XBVTFYABBZA2IP8LR'
secret_key = 'drrhgQOS7ffpAawfrMndih83O8FSHgfn1eOEjIUc'
trading_client = TradingClient(api_key, secret_key, paper=True)
account = trading_client.get_account()
# preparing orders


while(True):
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
  