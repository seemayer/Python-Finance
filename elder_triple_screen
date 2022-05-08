import pandas as pd
import os 
import add_indicators as ai

def df_from_csv(file): 
  df = pd.read_csv(file.path)
  df['Date'] = pd.to_datetime(df['Date'])
  df = df.set_index('Date')
  return df

def resample_weekly(df):

    # resample to weekly candles, i.e. five 1-day candles per business week
    dfw = df.Open.resample('W-MON').first().to_frame()
    dfw['Close'] = df.Close.resample('W-MON').last()
    dfw['High'] = df.High.resample('W-MON').max()
    dfw['Low'] = df.Low.resample('W-MON').min()
    dfw['Volume'] = df.Volume.resample('W-MON').sum()

    dfw = dfw.dropna()

    return dfw

#Reset screen passed list & empty files from folder
lst_screen1_passed = []
for file in os.scandir('screen passed'):
  os.unlink(file.path)

#Screen 1 - Weekly impulse
for file in os.scandir('./data/'):
  ticker = file.name[:-4] #remove .csv from filename
#   print(ticker)

  df = df_from_csv(file)
#   print(df)
  
  dfw = resample_weekly(df)
#   print(dfw)

  #calculate indicators for each ticker and add to dataframe
  dfw = ai.elder_impulse(dfw)
  dfw['screen_passed'] = dfw.impulse.ne('red')
#   print(dfw)

  #check last day to see if screen was passed
  screenpassed = any(dfw.screen_passed.tail(1))

  #save data as csv
  if screenpassed:
    lst_screen1_passed.append(ticker)

#Screen 2 - Daily Force index
for ticker in lst_screen1_passed:
  #calculate indicators for each ticker and add to dataframe
  screen_df = df.copy()
  screen_df = ai.force_index(screen_df)
  screen_df['screen_passed'] = screen_df.force_index.lt(0)

  #check last day to see if screen was passed
  screenpassed = any(screen_df.screen_passed.tail(1))
  if screenpassed:
    df.to_csv("./screen passed/" + ticker + ".csv")

print('screen complete')