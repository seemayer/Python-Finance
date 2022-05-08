import numpy as np
import pandas as pd
import get_stock_data as gd
import add_indicators as ai
import os 
from yahoo_fin import stock_info as si  # http://theautomatic.net/yahoo_fin-documentation/

def resample_weekly(df):

    # resample to weekly candles, i.e. five 1-day candles per business week
    dfw = df.Open.resample('W-MON').first().to_frame()
    dfw['Close'] = df.Close.resample('W-MON').last()
    dfw['High'] = df.High.resample('W-MON').max()
    dfw['Low'] = df.Low.resample('W-MON').min()
    dfw['Volume'] = df.Volume.resample('W-MON').sum()

    dfw = dfw.dropna()

    return dfw

def update_market_list():

  # Download list of market tickers and save to file
  tickers = si.tickers_ftse100() 
  # tickers = si.tickers_ftse250() 
  tickers = [item + '.L' for item in tickers]

  df = pd.DataFrame(data={"Ticker": tickers})
  df.to_csv("./config/market.csv", index=False)

# update_market_list()

# delete all files in screen passed folder
lst_screen_passed = []
lst_screen_passed2 = []

for file in os.scandir('screen passed'):
  os.unlink(file.path)
  
#pull list of tickers from market.csv file
df = pd.read_csv('config/market.csv')
lst_tickers = df['Ticker'].tolist()

# pull data for each ticker
for ticker in lst_tickers:
  print (ticker)
  
  try:
    df = gd.get_data(ticker)

    dfw = resample_weekly(df)

    #calculate indicators for each ticker and add to dataframe
    ai.elder_impulse(dfw)

    dfw['screen_passed'] = dfw.impulse.ne('red')

    #check last 5 days to see if screen was passed
    print(dfw.tail(5))
    screenpassed = any(dfw.screen_passed.tail(1))
    
    # save data as csv
    if screenpassed:
      lst_screen_passed.append(ticker)      

      #calculate indicators for each ticker and add to dataframe
      ai.force_index(df)

      df['screen_passed'] = df.force_index.lt(0)

      #check last 5 days to see if screen was passed
      print(df.tail(5))
      screenpassed2 = any(df.screen_passed.tail(1))
      if screenpassed2:
        lst_screen_passed2.append(ticker)      

  except:
    print("unable to pull data for "+ ticker)
  
# saving export list
df = pd.DataFrame(data={"stock": lst_screen_passed})
df.to_csv("./screen passed/SCREEN_PASSED.csv", sep=',',index=False)

df = pd.DataFrame(data={"stock": lst_screen_passed2})
df.to_csv("./screen passed/SCREEN_PASSED2.csv", sep=',',index=False)