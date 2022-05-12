import pandas as pd
import yfinance as yf
import os
import technical_indicators as ti
import market_data as md

returns_multiples = []
tickers = []

index_df = md.get_stock_data('^FTAS',period='1y', interval = '1d')

# Index Returns - (last close - first close)/first close
index_df = md.get_stock_data('^FTAS',period='1y', interval = '1d')
index_return = (index_df.Close[-1]-index_df.Close[0])/index_df.Close[0]+1
# print(index_df, index_return)

for file in os.scandir('./screen passed/'):
  
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

for file in os.scandir('./screen passed/'):
  # print(file.name, file.path)
    if file.name not in my_list:
      os.unlink(file.path)

