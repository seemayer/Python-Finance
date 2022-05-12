#!/usr/bin/env python3

# https://the7circles.uk/trading-for-a-living-5-market-indicators-and-trading-systems/


import os
import pandas as pd
import technical_indicators as ti
import market_data as md

for file in os.scandir('./screen passed/'):
  df = md.df_from_csv(file.path)
  print(f'ticker = {file.name[:-4]} , orderlevel = {ti.average_downside_penetration(df)}')