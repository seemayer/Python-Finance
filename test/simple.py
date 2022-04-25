import yfinance as yf
import finplot as fplt

df = yf.download('SPY',start='2018-01-01', end = '2020-04-29')
fplt.candlestick_ochl(df[['Open','Close','High','Low']])
fplt.plot(df.Close.rolling(50).mean())
fplt.plot(df.Close.rolling(200).mean())
fplt.show()