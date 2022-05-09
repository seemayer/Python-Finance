import pandas as pd
import yfinance as yf
import os
import add_indicators as ai

returns_multiples = []
tickers = []

def df_from_csv(file_path): 
  df = pd.read_csv(file_path)
  df['Date'] = pd.to_datetime(df['Date'])
  df = df.set_index('Date')
  return df

index_df = yf.download('^FTAS',period='1y', interval = '1d')

# Index Returns - (last close - first close)/first close
index_df = yf.download('^FTAS',period='1y', interval = '1d')
index_return = (index_df.Close[-1]-index_df.Close[0])/index_df.Close[0]+1
# print(index_df, index_return)

for file in os.scandir('./screen passed/'):
  
  tickers.extend([file.name[:-4]])

  # individual stock return
  stock_df = df_from_csv(file.path)
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

my_df = df_from_csv('./screen passed/ENOG.L.csv')
ai.force_index(my_df)
print(f'ENOG: \n {my_df}')
