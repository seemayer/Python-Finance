import market_data as md
import plot_object as plot
from datetime import datetime
import pandas as pd

# md.download_naked_trades()

df = md.df_from_csv('./my trades/trades.csv')

for index,row in df.iterrows():
    
    symbol = row.Symbol

    myplt = plot.myplot()
    myplt.create(symbol)
    df_stock_data = md.get_stock_data(symbol,period='5y')
    myplt.add_candles(df_stock_data)
    myplt.add_volume(df_stock_data)
    myplt.add_macd(df_stock_data)

        
    # print(index)
    if index>df_stock_data.index[0]: #only plot if in date range
        myplt.add_marker(df_stock_data,date = index,value=row.Buy_price, color='blue', name='Buy')
        myplt.add_hline(df_stock_data,start_date = index, length=50, value=row.Stop_price, color='red', width=2)
        myplt.add_hline(df_stock_data,start_date = index, length=50, value=row.Target_price, color='green', width=2)
        
    myplt.show()

        