

import pandas as pd
import yfinance as yf

def get_data(symbol):

  #symbol = 'GOOG SPY'
  interval = '1d'
  period = "1y"

  # load data and convert date
  df = yf.download(symbol,period=period, interval = interval)


  return df