import pandas as pd
import os 
import technical_indicators as ti
import market_data as md

md.del_dir_and_copy_files(src_dir = './data/', tar_dir = './screen passed/')

#Screen 1 - Weekly impulse
for file in os.scandir('./screen passed/'):
  
  df = md.df_from_csv(file.path)
  dfw = md.resample_weekly(df)

  #calculate indicators for each ticker and add to dataframe
  dfw = ti.add_elder_impulse(dfw)
  dfw['screen_passed'] = dfw.impulse.ne('red')

  #check last day to see if screen was passed
  screenpassed = any(dfw.screen_passed.tail(1))

  #delete files that do not pass the screen
  if not(screenpassed):
    os.unlink(file.path)

#Screen 2 - Daily Force index
for file in os.scandir('./screen passed/'):

  df = md.df_from_csv(file.path)

  #calculate indicators for each ticker and add to dataframe
  df = ti.add_force_index(df)
  df['screen_passed'] = df.force_index.lt(0)
  
  #check last day to see if screen was passed
  screenpassed = any(df.screen_passed.tail(1))
  
  if not(screenpassed):
    os.unlink(file.path)

print('triple screen complete')