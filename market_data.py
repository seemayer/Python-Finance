# stuff to run always here such as class/def

import os
import pandas as pd
import yfinance as yf
from yahoo_fin import stock_info as si
import shutil


def delete_files_in_dir(directory_name):  # Delete all files in a directory
    for file in os.scandir(directory_name):
        os.unlink(file.path)


def del_dir_and_copy_files(src_dir='./data/', tar_dir='./screen passed/'):
    try:
        shutil.rmtree(tar_dir)  # delete folder and all its contents
    except:
        print('Unable to delete folder')

    try:
        # getting all the files in the source directory
        files = os.listdir(src_dir)
        shutil.copytree(src_dir, tar_dir)
        print('Sucessfully copied data to screen passed folder')
    except:
        print('unable to copy over data')


def get_stock_data(ticker,
                   interval='1d',
                   period='1y'):  # download data from yahoo
    df = yf.download(ticker, period=period, interval=interval)
    return df


def download_SETS_tickers():

    MY_EXCEL_URL = "https://docs.londonstockexchange.com/sites/default/files/documents/list_of_sets_securities_103.xls"

    xl_df = pd.read_excel(MY_EXCEL_URL,
                          sheet_name='SETS',
                          skiprows=3,
                          usecols='B:V')
    xl_df = xl_df.dropna()
    xl_df = xl_df.query("Currency != 'USD'")
    lst_tickers = xl_df['Mnemonic'].to_list()
    lst_tickers = [item.replace('.', '')
                   for item in lst_tickers]  #remove periods
    # xl_df.to_csv('SETS.csv', index = False)
    # print(lst_tickers)
    return lst_tickers


def get_list_of_market_tickers(market):  # Download list of market tickers

  dict_markets = {
      'FTSE100': si.tickers_ftse100(),
      'FTSE250': si.tickers_ftse250(),
      'FTSE350': si.tickers_ftse100() + si.tickers_ftse250(),
      'SETS': download_SETS_tickers()
  }
  lst_tickers = dict_markets[market]
  lst_tickers = [item + '.L' for item in lst_tickers] #add suffix
  # print(lst_tickers)

  return lst_tickers


def save_stock_data_to_dir(lst_tickers, directory_name):
    for ticker in lst_tickers:

        try:
            print(ticker)
            df = get_stock_data(ticker)
            df.to_csv(directory_name + ticker + ".csv")
        except:
            print("unable to pull data for " + ticker)


def reset_market_data(directory_name='./data/', market='FTSE100'):
    delete_files_in_dir(directory_name)
    lst_tickers = get_list_of_market_tickers(market)
    save_stock_data_to_dir(lst_tickers, directory_name)
    print('Successfully downloaded market data and saved to folder')


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


def filter_files_in_dir(directory_name, filter_list):
    for file in os.scandir(directory_name):
        # print(file.name, file.path)
        if file.name not in filter_list:
            os.unlink(file.path)


if __name__ == "__main__":
    # stuff only to run when not called via 'import' here
    reset_market_data(directory_name='./data/', market='FTSE100')

#Populate the data folder with stock data based on a list of tickers
