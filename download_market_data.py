#Populate the data folder with stock data based on a list of tickers

import os
import yfinance as yf
from yahoo_fin import stock_info as si

def get_data(ticker,interval = '1d',period = '1y'):
  # download data from yahoo
  df = yf.download(ticker,period=period, interval = interval)
  return df

# Delete all files in data directory
for file in os.scandir('./data/'):
  os.unlink(file.path)

# Download list of market tickers and save to file
lst_tickers = si.tickers_ftse100() 
# lst_tickers = si.tickers_ftse250() 
lst_tickers = [item + '.L' for item in lst_tickers] #add suffix

for ticker in lst_tickers:
  
  try:
    print(ticker)
    df = get_data(ticker)
    df.to_csv("data/" + ticker + ".csv")
  except:
    print("unable to pull data for "+ ticker)
