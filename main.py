import pandas as pd
import get_data_and_save_to_csv as gd

#pull tickers from market.csv file

df = pd.read_csv('config/market.csv')
l1 = df['Ticker'].tolist()

#pull data for each ticker
for x in l1:
  print (x)
  gd.get_data(x)

#caculate indicators for each ticker

#screen based on indicators