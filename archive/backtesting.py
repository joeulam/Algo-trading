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
        pslow=90   # period for the slow moving average
    )

    def __init__(self):
        sma1 = bt.ind.SMA(period=self.p.pfast)  # fast moving average
        sma2 = bt.ind.SMA(period=self.p.pslow)  # slow moving average
        self.crossover = bt.ind.CrossOver(sma1, sma2)  # crossover signal

    def next(self):
        if not self.position:  # not in the market
            if self.crossover > 0:  # if fast crosses slow to the upside
                self.buy()  # enter long

        elif self.crossover < 0:  # in the market & cross to the downside
            self.close()  # close long position


cerebro = bt.Cerebro()  # create a "Cerebro" engine instance

# Create a data feed
data = bt.feeds.PandasData(dataname=yf.download('ETH-USD',
                                                    start=datetime.datetime(2018, 1, 21),
                                                    end=datetime.datetime(2023, 9, 21),
                                                    progress=False))
cerebro.adddata(data)  # Add the data feed

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