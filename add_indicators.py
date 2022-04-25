#https://github.com/highfestiva/finplot/blob/master/finplot/examples/analyze.py


import pandas as pd
import numpy as np

def ema(df, period):
  df[str(period) + 'EMA'] = df.Close.ewm(span=period).mean()

def macd(df):
  # add MACD, Signal and histogram (diff)
  df['macd'] = df.Close.ewm(span=12).mean() - df.Close.ewm(span=26).mean()
  df['signal'] = df.macd.ewm(span=9).mean()
  df['macd_diff'] = df.macd - df.signal

def macd_crossover(df):
  macd(df) #requires macd columns to be added to df
    
  # 2 represents cross above, -2 cross below
  df['crossover'] = np.sign(df.macd_diff).diff()