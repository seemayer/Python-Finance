#!/usr/bin/env python3

# https://the7circles.uk/trading-for-a-living-5-market-indicators-and-trading-systems/


import os
import pandas as pd
import add_indicators as ai

def df_from_csv(file_path): 
  df = pd.read_csv(file_path)
  df['Date'] = pd.to_datetime(df['Date'])
  df = df.set_index('Date')
  return df

for file in os.scandir('./screen passed/'):
  df = df_from_csv(file.path)
  print(f'ticker = {file.name[:-4]} , orderlevel = {ai.OrderLevel_ADP(df)}')