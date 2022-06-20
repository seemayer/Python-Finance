# stuff to run always here such as class/def

import config
import os
import pandas as pd
import yfinance as yf
from yahoo_fin import stock_info as si
import shutil
import requests
from datetime import datetime

## Naked Trades ##
def download_naked_trades(earliest_date='2017-01-01'):
    # https://stackoverflow.com/questions/10556048/how-to-extract-tables-from-websites-in-python
    url = 'https://www.nakedtrader.co.uk/agree.htm?agree=1'
    html = requests.get(url).content
    df_list = pd.read_html(html)

    # clean up data
    dict_from_csv = pd.read_csv('./naked trades/MAP.csv', header=0, index_col=0).squeeze('columns').to_dict()
    for i in range(2):
        df_list[i].rename(columns = {'Buy Date':'Date'}, inplace = True) #rename for indexing
        df_list[i]['Date'] = pd.to_datetime(df_list[i]['Date'], format = '%d/%m/%Y', errors = 'coerce') #ensure UK date format , '%d/%m/%Y'
        df_list[i] = df_list[i][(df_list[i]['Date'] > earliest_date)] #cutoff date
        df_list[i]['Sell Date'] = pd.to_datetime(df_list[i]['Sell Date'], format = '%d/%m/%Y', errors = 'coerce') #ensure UK date format , '%d/%m/%Y'
        
        df_list[i]['Epic'] = df_list[i]['Epic'].str.upper() #uppercase before replacing
        df_list[i]['Epic'] = df_list[i]['Epic'].replace(dict_from_csv) #replace bad/delisted tickers
        df_list[i] = df_list[i].dropna(subset = 'Epic') #drop null tickers
        df_list[i] = df_list[i].dropna(subset = 'Date') #drop null dates
        df_list[i] = df_list[i][df_list[i].Epic != 'Delisted'] #drop delisted tickers
    
    df_Shares = df_list[0]
    df_Spread_Longs = df_list[1]
    df_Spread_Shorts = df_list[2]

    df_Shares.to_csv('./naked trades/Shares.csv', index=False)
    df_Spread_Longs.to_csv('./naked trades/Spread_Longs.csv', index=False)
    df_Spread_Shorts.to_csv('./naked trades/Spread_Shorts.csv', index=False)

    print(f'naked trades downloaded from {earliest_date}')

## Handle Files ##
def delete_files_in_dir(directory_name):  # Delete all files in a directory
    for file in os.scandir(directory_name):
        os.unlink(file.path)
    print(f'Files in {directory_name} deleted')

def del_dir_and_copy_files(src_dir = config.DATA_DIR, tar_dir = config.SCREEN_DIR):
    
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

def save_stock_data_to_dir(lst_tickers, directory_name):
    #Populate the data folder with stock data based on a list of tickers
    for ticker in lst_tickers:

        try:
            print(ticker)
            df = get_stock_data(ticker)
            df.to_csv(directory_name + ticker + ".csv")
        except:
            print("unable to pull data for " + ticker)

def filter_files_in_dir(directory_name, filter_list):
    for file in os.scandir(directory_name):
        # print(file.name, file.path)
        if file.name not in filter_list:
            os.unlink(file.path)

## Get Data ##
def get_stock_data(ticker, interval=config.INTERVAL, period=config.PERIOD):
    # download data from yahoo
    if config.START == None or config.END == None:
        df = yf.download(ticker, period=period, interval=interval)

        print('period')
    else:
        df = yf.download(ticker,
                         interval=interval,
                         start=config.START,
                         end=config.END)
        print('start end')
    
    return df

def df_from_csv(file_path):
    # pull some data - when writing and reading back from csv the index is converted to an object type so need to convert back to datetime64 if to be used with finplot
    df = pd.read_csv(file_path)
    # df.Date = pd.to_datetime(df.Date, format='%d/%m/%Y') #ensure UK date format
    
    # format it in pandas
    df = df.astype({'Date':'datetime64[ns]'})
    df = df.set_index('Date')
    # print(f'Dataframe:\n{df}\ndf datatypes:\n{df.dtypes}')
    return df

def download_SETS_tickers():

    # download list of SETS tickers excluding investment trusts
    MY_EXCEL_URL = "https://docs.londonstockexchange.com/sites/default/files/documents/list_of_sets_securities_103.xls"

    xl_df = pd.read_excel(MY_EXCEL_URL,
                          sheet_name='SETS',
                          skiprows=3,
                          usecols='B:V')
    xl_df = xl_df.dropna()
    xl_df = xl_df.query("`Currency` != 'USD'")  # remove listings in USD

    # Filter out investment trusts
    lst_IT = get_investment_trust_codes()
    xl_df = xl_df.query("`ISIN` not in @lst_IT")
    # xl_df.to_csv('SETS.csv', index = False)

    lst_tickers = xl_df['Mnemonic'].to_list()

    return lst_tickers

def get_investment_trust_codes():

    MY_EXCEL_URL = "https://docs.londonstockexchange.com/sites/default/files/reports/Instrument%20list_23.xlsx"

    xl_df = pd.read_excel(MY_EXCEL_URL,
                          sheet_name='1.0 All Equity',
                          skiprows=7,
                          usecols='A:O')

    xl_df = xl_df.query(
        "`FCA Listing Category` == 'Premium Equity Closed Ended Investment Funds'"
    )
    lst_IT_ISIN = xl_df['ISIN'].to_list()

    return lst_IT_ISIN

def get_list_of_market_tickers(market):  # Download list of market tickers

    dict_markets = {
        'FTSE100': si.tickers_ftse100(),
        'FTSE250': si.tickers_ftse250(),
        'FTSE350': si.tickers_ftse100() + si.tickers_ftse250(),
        'SETS': download_SETS_tickers()
    }
    lst_tickers = dict_markets[market]
    #remove periods from end
    lst_tickers = [
        item[:-1] if item[-1] == '.' else item for item in lst_tickers
    ]
    #replace internal dots with dashes to get yahoo format
    lst_tickers = [item.replace('.', '-') for item in lst_tickers]
    #add suffix
    lst_tickers = [item + '.L' for item in lst_tickers]
    # print(lst_tickers)
    # print(f'{market} Tickers downloaded')

    return lst_tickers

## Resample Data ##

def resample_daily(df_weekly):

    # resample to weekly candles, i.e. five 1-day candles per business week
    df_daily = df_weekly.resample('D').ffill()

    # df_daily = df_daily.dropna()

    return df_daily

def resample_weekly(df):

    # resample to weekly candles, i.e. five 1-day candles per business week
    dfw = df.Open.resample('W-MON').first().to_frame()
    dfw['Close'] = df.Close.resample('W-MON').last()
    dfw['High'] = df.High.resample('W-MON').max()
    dfw['Low'] = df.Low.resample('W-MON').min()
    dfw['Volume'] = df.Volume.resample('W-MON').sum()

    dfw = dfw.dropna()

    return dfw

## Routines ##

def reset_market_data(directory_name=config.DATA_DIR, lst_tickers=['VOD.L', '888.L']):
    delete_files_in_dir(directory_name)
    save_stock_data_to_dir(lst_tickers, directory_name)
    print(f'Successfully downloaded market data and saved to {directory_name}')

if __name__ == "__main__":
    # stuff only to run when not called via 'import' here
    reset_market_data()
    



