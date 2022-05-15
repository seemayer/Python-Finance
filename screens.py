import config
import pandas as pd
import os 
import technical_indicators as ti
import market_data as md
import yfinance as yf

def elder_triple():
  
  md.del_dir_and_copy_files(src_dir = config.DATA_DIR, tar_dir = config.SCREEN_DIR)
  
  #Screen 1 - Weekly impulse
  for file in os.scandir(config.SCREEN_DIR):
    
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
  for file in os.scandir(config.SCREEN_DIR):
  
    df = md.df_from_csv(file.path)
  
    #calculate indicators for each ticker and add to dataframe
    df = ti.add_force_index(df)
    df['screen_passed'] = df.force_index.lt(0)
    
    #check last day to see if screen was passed
    screenpassed = any(df.screen_passed.tail(1))
    
    if not(screenpassed):
      os.unlink(file.path)
  
  print('triple screen complete')

def elder_divergence():

  md.del_dir_and_copy_files(src_dir = config.DATA_DIR, tar_dir = config.SCREEN_DIR) 
  # delete all files in screen passed folder
  lst_screen_passed = []
  
  # md.del_dir_and_copy_files(src_dir = './data/', tar_dir = './screen passed/')
  
  #Screen 1 - Weekly impulse
  for file in os.scandir(config.SCREEN_DIR):
  
    df = md.df_from_csv(file.path)
  
    #calculate indicators for each ticker and add to dataframe
    try:
      df = ti.add_elder_bull_divergence(df, period=40)
  
      #check last 5 days to see if screen was passed
      screenpassed = any(df.divergence.tail(5))
      print(file.name)
    
      # save data as csv
      if screenpassed:
        lst_screen_passed.append(file.name)
    except:
      print(f'Unable to calc for {file.name}')
    
  # saving export list
  df = pd.DataFrame(data={"stock": lst_screen_passed})
  df.to_csv("./SCREEN_PASSED.csv", sep=',',index=False)
  
  print(lst_screen_passed)
  
  md.filter_files_in_dir(config.SCREEN_DIR,lst_screen_passed)

def relative_strength():
  returns_multiples = []
  tickers = []
      
  # Index Returns - (last close - first close)/first close
  index_df = md.get_stock_data(ticker='^FTAS')
  index_return = (index_df.Close[-1]-index_df.Close[0])/index_df.Close[0]+1
  # print(index_df, index_return)
  
  for file in os.scandir(config.SCREEN_DIR):
    
    tickers.extend([file.name[:-4]])
  
    # individual stock return
    stock_df = md.df_from_csv(file.path)
    stock_return = (stock_df.Close[-1]-stock_df.Close[0])/stock_df.Close[0]+1
  
    # return relative to market
    returns_multiple = round((stock_return / index_return), 2)
    returns_multiples.extend([returns_multiple])
      
  #   print (f'Ticker: {file.name[:-4]}; Returns Multiple against FTSE All Share: {returns_multiple}')
  
  # Creating dataframe of only top 30%
  rs_df = pd.DataFrame(list(zip(tickers, returns_multiples)), columns=['Ticker', 'Returns_multiple'])
  rs_df['RS_Rating'] = rs_df.Returns_multiple.rank(pct=True) * 100
  rs_df = rs_df[rs_df.RS_Rating >= rs_df.RS_Rating.quantile(.70)]
  
  print('Top 30% relative strength: \n',rs_df)
  
  my_list = rs_df.Ticker.tolist()
  my_list = [item + '.csv' for item in my_list] #add suffix
  print(my_list)
  
  md.filter_files_in_dir(config.SCREEN_DIR, my_list)

if __name__ == "__main__":
  # stuff only to run when not called via 'import' here
  pass
