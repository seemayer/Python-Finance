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

def elder_impulse(df):
  macd(df) #requires macd columns to be added to df
  ema(df,22) #requires ema

  #https://www.dataquest.io/blog/tutorial-add-column-pandas-dataframe-based-on-if-else-condition/
  # create a list of our conditions
  conditions = [
      (df.macd_diff.diff().gt(0) & df['22EMA'].diff().gt(0)), #green
      (df.macd_diff.diff().lt(0) & df['22EMA'].diff().lt(0)), #red
      (df.macd_diff.diff().gt(0) & df['22EMA'].diff().lt(0)), #blue
      (df.macd_diff.diff().lt(0) & df['22EMA'].diff().gt(0))  #blue
      ]
  
  # create a list of the values we want to assign for each condition
  values = ['green', 'red', 'blue', 'blue']
  
  # create a new column and use np.select to assign values to it using our lists as arguments
  df['impulse'] = np.select(conditions, values)
  
def elder_divergence(df,period):
  
  macd(df) #requires macd columns to be added to df

  df["lowestMACD100"] = df['macd_diff'].rolling(period).min()
  df["condition1"] = df.lowestMACD100 == df.macd_diff
  
  # display updated DataFrame
  #df.head()
      
  