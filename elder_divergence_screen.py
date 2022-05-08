import pandas as pd
import get_stock_data as gd
import add_indicators as ai
import os 
from yahoo_fin import stock_info as si  # http://theautomatic.net/yahoo_fin-documentation/

def update_market_list():

  # Download list of market tickers and save to file
  # tickers = si.tickers_ftse100() 
  tickers = si.tickers_ftse250() 
  tickers = [item + '.L' for item in tickers]

  df = pd.DataFrame(data={"Ticker": tickers})
  df.to_csv("./config/market.csv", index=False)

update_market_list()

# delete all files in screen passed folder
lst_screen_passed = []

for file in os.scandir('screen passed'):
  os.unlink(file.path)
  
#pull list of tickers from market.csv file
df = pd.read_csv('config/market.csv')
lst_tickers = df['Ticker'].tolist()

#pull data for each ticker
for ticker in lst_tickers:
  print (ticker)
  
  try:
    df = gd.get_data(ticker)

    #calculate indicators for each ticker and add to dataframe
    ai.elder_divergence(df, period=40)

    #check last 5 days to see if screen was passed
    screenpassed = any(df.screen_passed.tail(5))
    
    # save data as csv
    if screenpassed:
      df.to_csv("screen passed/" + ticker + ".csv")
      lst_screen_passed.append(ticker)      
    else:
      df.to_csv("data/" + ticker + ".csv")
  except:
    print("unable to pull data for "+ ticker)
  
# saving export list
df = pd.DataFrame(data={"stock": lst_screen_passed})
df.to_csv("./screen passed/SCREEN_PASSED.csv", sep=',',index=False)