import backtrader as bt
import datetime
import config
import yfinance as yf
import datetime
# Create a subclass of Strategy to define the indicators and logic

class SmaCross(bt.Strategy):
    # list of parameters which are configurable for the strategy
    params = dict(
        pfast=30,  # period for the fast moving average
        pslow=90,   # period for the slow moving average
        rsi_period = 14 #period for RSI
        
    )

    def __init__(self):
        self.sma1 = bt.indicators.SimpleMovingAverage(
            self.data.close, period=self.params.pfast
        )
        self.sma2 = bt.indicators.SimpleMovingAverage(
            self.data.close, period=self.params.pslow
        )

        self.rsi = bt.indicators.RelativeStrengthIndex(period=self.params.rsi_period)

    def next(self):
        def fiveTrend():
            i = -5
            total = 0 
            while(i < 0):
                total += self.data.close[i]
                i -= 1
                return total / 5 
        price = self.data.close[0]

        if not self.position:  # not in the market 

            if self.sma1 >= self.sma2 and fiveTrend() < price:
                self.buy_condition_triggered = True
                self.sell_condition_triggered = False
                self.buy(price=price)

        elif self.sma1 <= self.sma2: #and fiveTrend() < price
            self.sell_condition_triggered = True
            self.buy_condition_triggered = False
            self.close()
              # close long position


cerebro = bt.Cerebro()  # create a "Cerebro" engine instance

# Create a data feed
data = bt.feeds.PandasData(dataname=yf.download('ETH-USD',
                                                    start=datetime.datetime(2023, 1, 21),
                                                    end=datetime.datetime(2023, 9, 21),
                                                    progress=False))
cerebro.adddata(data)

cerebro.addstrategy(SmaCross)  # Add the trading strategy
print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
initial_portfolio_value = cerebro.broker.getvalue()
cerebro.run()
final_portfolio_value = cerebro.broker.getvalue()
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
percentage_change = ((final_portfolio_value - initial_portfolio_value) / initial_portfolio_value) * 100
print("Precent changed: " + str(percentage_change))
cerebro.plot(style='pnl')  # Use 'candlestick' style for OHLC plot
plt.show() # and plot it with a single command