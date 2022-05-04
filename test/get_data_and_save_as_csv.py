import pandas as pd
import yfinance as yf

symbol = 'ABDP.L'

interval = '1d'
period = "1y"

# download data from yahoo
df = yf.download(symbol,period=period, interval = interval)
df.insert(0,'Ticker',symbol)

df.to_csv('./' + symbol + '.csv')