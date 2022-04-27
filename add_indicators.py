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

def macd_cross(df):
  macd(df) #requires macd columns to be added to df
    
  # 2 represents cross above, -2 cross below
  df['crossover'] = np.sign(df.macd_diff).diff()>0
  df['crossunder'] = np.sign(df.macd_diff).diff()<0

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
  
  macd = df.Close.ewm(span=12).mean() - df.Close.ewm(span=26).mean()
  signal = macd.ewm(span=9).mean()
  df['macd_diff'] = macd - signal

  df['lowest_MACD'] = df.macd_diff.rolling(period).min()
  df['MACD_ratio'] = (df.macd_diff/df.lowest_MACD).where(df.macd_diff.lt(0), 0)
  df['lowest_Low'] = df.Low.rolling(period).min()
  df['crossunder'] = np.sign(df.macd_diff).diff().lt(0)
  df['MACD_up'] = np.sign(df.macd_diff.diff()).gt(0)
 
# // Bullish divergence

  df.loc[df.index[0],'state'] = '0'
  df.at[df.index[0],'state'] = [0,0,0,0]

  for i in range(1, len(df)):

    newstate = df.loc[df.index[i-1],'state']
    if (newstate == [0,0,0,1]):
      newstate = [1,0,0,0]

    
    # # // if todays MACD is the lowest in the last 'nodays' days then trigger condition 1 and reset other conditions
    if (df.loc[df.index[i],'macd_diff'] == df.loc[df.index[i],'lowest_MACD']):
      newstate = [1,0,0,0]
      
    # # // if condition 1 has been triggered (in a prior period) then if MACD crosses below zero then trigger condition 2
    if ((newstate == [1,0,0,0]) & (df.loc[df.index[i],'crossunder']==True)):
      newstate = [0,1,0,0]
    
    # // if both condition 1 & 2 have been triggered in order (in a prior period) then if price hits new lows then trigger condition 3
    if ((newstate == [0,1,0,0]) & (df.loc[df.index[i],'Low'] == df.loc[df.index[i],'lowest_Low'])):
      newstate = [0,0,1,0]    
      
    # // if conditions 1, 2 & 3 have been triggered in that order then check if the MACD ticks upwards and issue a signal if so
    if ((newstate == [0,0,1,0]) & (df.loc[df.index[i],'MACD_up'] == True) &(df.loc[df.index[i],'MACD_ratio'] < 0.5)):
      newstate = [0,0,0,1]    
    
    df.at[df.index[i],'state'] = newstate

