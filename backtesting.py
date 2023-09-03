import backtrader as bt
import datetime
import config
import yfinance as yf
import datetime

class MyStrategy(bt.Strategy):

    params = (
        ("short_period", 10),   # Short SMA period
        ("long_period", 20),  # Long SMA period
        ("rsi_period", 14),   # RSI period
        ("rsi_overbought", 70),  # RSI overbought threshold
        ("rsi_oversold", 40),     # RSI oversold threshold
    )

    def __init__(self):
        self.short_sma = bt.indicators.SimpleMovingAverage(
            self.data.close, period=self.params.short_period
        )
        self.long_sma = bt.indicators.SimpleMovingAverage(
            self.data.close, period=self.params.long_period
        )
        self.rsi = bt.indicators.RelativeStrengthIndex(period=self.params.rsi_period)
        self.buy_condition_triggered = False
        self.sell_condition_triggered = False
    
    def next(self):
        def fiveTrend():
            i = -5
            total = 0 
            while(i < 0):
                total += self.data.close[i]
                i -= 1
                return total / 5 
        price = self.data.close[0]
        if self.short_sma >= self.long_sma and (self.rsi <= self.params.rsi_oversold or fiveTrend() > price ):
            self.buy_condition_triggered = True
            self.sell_condition_triggered = False
            self.buy(price=price)
        elif self.short_sma <= self.long_sma and (self.rsi >= self.params.rsi_overbought): #and fiveTrend() < price
            self.sell_condition_triggered = True
            self.buy_condition_triggered = False
            self.sell(price=price)

if __name__ == '__main__':
    cerebro = bt.Cerebro()
    
    # Load historical data (replace with your data source)
    data = bt.feeds.PandasData(dataname=yf.download('ETH-USD',
                                                    start=datetime.datetime(2022, 1, 1),
                                                    end=datetime.datetime(2023, 9, 1),
                                                    progress=False))
    cerebro.adddata(data)

    cerebro.addstrategy(MyStrategy)

    cerebro.broker.set_cash(2000)  # Set an initial cash balance
    cerebro.addsizer(bt.sizers.FixedSize, stake=1)  # Set initial position size to 0

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    initial_portfolio_value = cerebro.broker.getvalue()
    cerebro.run()
    final_portfolio_value = cerebro.broker.getvalue()
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    percentage_change = ((final_portfolio_value - initial_portfolio_value) / initial_portfolio_value) * 100
    print("Precent changed: " + str(percentage_change))
    cerebro.plot(style='pnl')  # Use 'candlestick' style for OHLC plot
    plt.show()