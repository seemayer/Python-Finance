import pandas as pd
import yfinance as yf

def get_data(symbol):

  interval = '1d'
  period = "1y"

  # download data from yahoo
  df = yf.download(symbol,period=period, interval = interval)

  return df