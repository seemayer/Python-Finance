import pandas as pd
import yfinance as yf

symbol = 'MSFT'
interval = '1mo'
period = "2y"

# load data and convert date
df = yf.download(symbol,period=period, interval = interval)

df.to_csv(symbol + ".csv")