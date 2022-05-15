#!/usr/bin/env python3

# https://the7circles.uk/trading-for-a-living-5-market-indicators-and-trading-systems/

import config
import os
import pandas as pd
import technical_indicators as ti
import market_data as md

def order_levels():

  d = []
  for file in os.scandir(config.SCREEN_DIR):
    df = md.df_from_csv(file.path)  
    d.append(
          {
              'Ticker': file.name[:-4],
              'Order Level': ti.average_downside_penetration(df),
              'Stop Level': ti.chandelier_exit_long(df)
          }
      )
  
  out_df = pd.DataFrame(d)
  print(out_df)
  out_df.to_csv('OUTPUT.csv', index = False)


  
 

  
  # for file in os.scandir('./screen passed/'):
  #   df = md.df_from_csv(file.path)
  #   print(f'ticker = {file.name[:-4]} , orderlevel = {ti.average_downside_penetration(df)}, stoplevel = {ti.chandelier_exit_long(df)}')




