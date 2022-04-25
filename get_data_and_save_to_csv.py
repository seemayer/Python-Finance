import pandas as pd
import yfinance as yf

symbol = 'TSLA'
interval = '1d'
period = "2y"

# load data and convert date
df = yf.download(symbol,period=period, interval = interval)
print(df.tail[6])