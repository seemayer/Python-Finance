

import pandas as pd
import yfinance as yf

def get_data(symbol):

  #symbol = 'GOOG SPY'
  interval = '1mo'
  period = "2y"

  # load data and convert date
  df = yf.download(symbol,period=period, interval = interval)

  df.to_csv("data/" + symbol + ".csv")
  return