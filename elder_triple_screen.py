import pandas as pd
import os 
import add_indicators as ai
import shutil


def reset_screen_files():
  try:
    shutil.rmtree('./screen passed/') # delete folder and all its contents
  except:
    print('Unable to delete folder')

  try:
    # copy files from data folder
    src_dir = './data/'
    dest_dir = './screen passed/'
    # getting all the files in the source directory
    files = os.listdir(src_dir)
    shutil.copytree(src_dir, dest_dir)
    print('Sucessfully copied data to screen passed folder')
  except:
    print('unable to copy over data')
def df_from_csv(file_path): 
  df = pd.read_csv(file_path)
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

reset_screen_files()

#Screen 1 - Weekly impulse
for file in os.scandir('./screen passed/'):
  
  df = df_from_csv(file.path)
  dfw = resample_weekly(df)

  #calculate indicators for each ticker and add to dataframe
  dfw = ai.elder_impulse(dfw)
  dfw['screen_passed'] = dfw.impulse.ne('red')

  #check last day to see if screen was passed
  screenpassed = any(dfw.screen_passed.tail(1))

  #delete files that do not pass the screen
  if not(screenpassed):
    os.unlink(file.path)

#Screen 2 - Daily Force index
for file in os.scandir('./screen passed/'):

  df = df_from_csv(file.path)

  #calculate indicators for each ticker and add to dataframe
  df = ai.force_index(df)
  df['screen_passed'] = df.force_index.lt(0)
  
  #check last day to see if screen was passed
  screenpassed = any(df.screen_passed.tail(1))
  
  if not(screenpassed):
    os.unlink(file.path)

print('screen complete')