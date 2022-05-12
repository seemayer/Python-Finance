# stuff to run always here such as class/def

import os
import pandas as pd
import yfinance as yf
from yahoo_fin import stock_info as si
import shutil

def delete_files_in_dir(directory_name): # Delete all files in a directory
  for file in os.scandir(directory_name):
    os.unlink(file.path)

def del_dir_and_copy_files(src_dir = './data/', tar_dir = './screen passed/'):
  try:
    shutil.rmtree(tar_dir) # delete folder and all its contents
  except:
    print('Unable to delete folder')
    
  try:
  # getting all the files in the source directory
    files = os.listdir(src_dir)
    shutil.copytree(src_dir, tar_dir)
    print('Sucessfully copied data to screen passed folder')
  except:
    print('unable to copy over data')


def get_stock_data(ticker, interval = '1d', period = '1y'): # download data from yahoo
  df = yf.download(ticker, period = period, interval = interval)
  return df

def get_list_of_market_tickers(market): # Download list of market tickers
  if market == 'FTSE100':
    lst_tickers = si.tickers_ftse100() 
  elif market == 'FTSE250':
    lst_tickers = si.tickers_ftse250()
  elif market == 'FTSE350':
    lst_tickers = si.tickers_ftse100() + si.tickers_ftse250()

  lst_tickers = [item + '.L' for item in lst_tickers] #add suffix
  return lst_tickers

def save_stock_data_to_dir(lst_tickers, directory_name):
  for ticker in lst_tickers:
    
    try:
      print(ticker)
      df = get_stock_data(ticker)
      df.to_csv(directory_name + ticker + ".csv")
    except:
      print("unable to pull data for " + ticker)

def reset_market_data(directory_name = './data/', market = 'FTSE100'):
  delete_files_in_dir(directory_name)
  lst_tickers = get_list_of_market_tickers(market)
  save_stock_data_to_dir(lst_tickers, directory_name)

def df_from_csv(file_path): 
  # when writing and reading back from csv the index is converted to an object type so need to convert back to datetime64 if to be used with finplot
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

if __name__ == "__main__":
   # stuff only to run when not called via 'import' here
   reset_market_data(directory_name = './data/', market = 'FTSE100')


   
   













#Populate the data folder with stock data based on a list of tickers




