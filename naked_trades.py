import market_data as md
import plot_object as plot
from datetime import datetime
import pandas as pd

# md.download_naked_trades()

df = md.df_from_csv('./naked trades/Shares.csv')

# filter on only SETS traded stocks
SETS_tickers = md.get_list_of_market_tickers('SETS')
SETS_tickers = [s.replace('.L','') for s in SETS_tickers]
df = df[df['Epic'].isin(SETS_tickers)]

unique = df['Epic'].unique()
print(unique)
start_pos = 0

for idi, i in enumerate(unique[start_pos:]):
    
    newdf = df[(df['Epic']==i)]
    print(newdf)
    print(f'idi = {idi + start_pos}')
    symbol = i + '.L'

    myplt = plot.myplot()
    myplt.create(symbol)
    df_stock_data = md.get_stock_data(symbol,period='5y')
    myplt.add_candles(df_stock_data)
    myplt.add_volume(df_stock_data)
    myplt.add_macd(df_stock_data)

    buy_legend_flag = True
    sell_legend_flag = True
    for index,row in newdf.iterrows():
        
        # print(index)
        if index>df_stock_data.index[0]: #only plot if in date range
            myplt.add_marker(df_stock_data,date = index,value=row.Price, color='blue', name=('Buy' if buy_legend_flag else None))
            myplt.add_hline(df_stock_data,start_date = index, length=50, value=row.Stop, color='red', width=2)
            myplt.add_hline(df_stock_data,start_date = index, length=50, value=row.Target, color='green', width=2)
            if not pd.isnull(row['Sell Date']):
                myplt.add_marker(df_stock_data,date = row['Sell Date'],value=row.Sell, color='yellow', name=('Sell' if sell_legend_flag else None))
                sell_legend_flag = False
            buy_legend_flag = False
        
    myplt.show()

        