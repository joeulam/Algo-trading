from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.trading.client import TradingClient

api_key = 'PK1XBVTFYABBZA2IP8LR'
secret_keys = 'drrhgQOS7ffpAawfrMndih83O8FSHgfn1eOEjIUc'
url = 'https://data.sandbox.alpaca.markets/v2'

trading_client = TradingClient(api_key, secret_keys, paper=True)
account = trading_client.get_account()


alpaca.data.live.crypto.CryptoDataStream(api_key,secret_keys,secret_keys)


# preparing orders
while(True):
  if()
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