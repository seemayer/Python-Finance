import pandas as pd
import get_stock_data as gd
import add_indicators as ai
import plot as plt
import os 


# http://theautomatic.net/yahoo_fin-documentation/
# update list of market tickers
# from yahoo_fin import stock_info as si
# # tickers = si.tickers_ftse100() 
# tickers = si.tickers_ftse250() 
# tickers = [item + '.L' for item in tickers]

# df = pd.DataFrame(data={"Ticker": tickers})
# df.to_csv("./config/market.csv", index=False)



exportList = []

# delete all files in screen passed folder
for file in os.scandir('screen passed'):
  os.unlink(file.path)
  
#pull list of tickers from market.csv file

df = pd.read_csv('config/market.csv')
l1 = df['Ticker'].tolist()

#pull data for each ticker
for symbol in l1:
  print (symbol)
  df = gd.get_data(symbol)

  #caculate indicators for each ticker
  
  #ai.ema(df,100)
  #ai.macd(df)
  #ai.macd_cross(df)
  #ai.elder_impulse(df)
  ai.elder_divergence(df, period=40)

  #screen based on indicators
  
  #check last 5 days to see if screen was passed
  screenpassed = any(df.screen_passed.tail(5))
  
  # save data as csv
  if screenpassed:
    df.to_csv("screen passed/" + symbol + ".csv")
    exportList.append(symbol)
    
  else:
    df.to_csv("data/" + symbol + ".csv")

  
# saving export list
df = pd.DataFrame(data={"stock": exportList})
df.to_csv("./screen passed/PASSED.csv", sep=',',index=False)

#plot chart

# plt.plot_chart('SBRY.L', '1d')

