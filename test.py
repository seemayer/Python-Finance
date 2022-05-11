<<<<<<< HEAD
=======
#!/usr/bin/env python3

# https://the7circles.uk/trading-for-a-living-5-market-indicators-and-trading-systems/

import get_stock_data as gsd
import os
>>>>>>> e36b7445276333e944a7be50c5266327a58141f6
import pandas as pd
import numpy as np
import add_indicators as ai

<<<<<<< HEAD
def letgo(df = df):
    df.drop('b', axis=1, inplace=True)

frm = pd.DataFrame({'a':[1,2], 'b':[3,4]})
print(frm)
letgo(frm)  # will alter frm
print(frm)


=======
def df_from_csv(file_path): 
  df = pd.read_csv(file_path)
  df['Date'] = pd.to_datetime(df['Date'])
  df = df.set_index('Date')
  return df

for file in os.scandir('./screen passed/'):
  df = df_from_csv(file.path)
  print(f'ticker = {file.name[:-4]} , orderlevel = {ai.OrderLevel_ADP(df)}')
>>>>>>> e36b7445276333e944a7be50c5266327a58141f6
