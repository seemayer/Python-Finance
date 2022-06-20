import market_data as md
import plot_object as plot
from datetime import datetime
import pandas as pd

# md.download_naked_trades()

df = md.df_from_csv('./naked trades/Shares.csv')

#clean up any incorrect tickers
df =  df.replace({'Epic':{'T17':'TM17'}})

df['Sell Date'] = pd.to_datetime(df['Sell Date'], format='%d/%m/%Y', errors='coerce') #ensure UK date format , '%d/%m/%Y'

unique = df['Epic'].unique()
# print(unique)

for i in unique:
    
    newdf = df[(df['Epic']==i)]
    print(newdf)
    symbol = i + '.L'

    myplt = plot.myplot()
    myplt.create(symbol)
    df_stock_data = md.get_stock_data(symbol,period='5y')
    myplt.add_candles(df_stock_data)
    myplt.add_macd(df_stock_data)

    for index,row in newdf.iterrows():
        # print(index)
        if index>df_stock_data.index[0]: #only plot if in date range
            myplt.add_marker(df_stock_data,date = index,value=row.Price)
            myplt.add_hline(df_stock_data,start_date = index, length=50, value=row.Stop, color='red')
            myplt.add_hline(df_stock_data,start_date = index, length=50, value=row.Target, color='green')
            if not pd.isnull(row['Sell Date']):
                myplt.add_marker(df_stock_data,date = row['Sell Date'],value=row.Sell, color='yellow', name='Sell')
        
    myplt.show()

        