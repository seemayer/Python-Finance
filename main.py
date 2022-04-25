import pandas as pd
import get_stock_data as gd
import add_indicators as ai
import plot as plt

#pull tickers from market.csv file

df = pd.read_csv('config/market.csv')
l1 = df['Ticker'].tolist()

#pull data for each ticker
for symbol in l1:
  print (symbol)
  df = gd.get_data(symbol)

  #caculate indicators for each ticker
  
  #ai.ema(df,100)
  #ai.macd(df)
  #ai.macd_crossover(df)
  ai.elder_impulse(df)
  
  
  
  
  df.to_csv("data/" + symbol + ".csv")

  

#screen based on indicators

#plot chart


#plt.plot_chart('GOOG', '1d')

