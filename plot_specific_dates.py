#!/usr/bin/env python3

import finplot as fplt
import yfinance as yf
import datetime
import market_data as md
import pandas as pd




def plot_specific_dates(symbol="VOD.L", start_date='2021-01-01', end_date='2021-12-31',buy_price=1, stop_price=1, target_price=1):

    df = yf.download(symbol)


    df = df.reset_index(level=0)
    df = df.set_index('Date')  

    xmin = datetime.datetime.strptime(start_date, "%Y-%m-%d").timestamp()
    xmax = datetime.datetime.strptime(end_date, "%Y-%m-%d").timestamp()

    ax = fplt.create_plot(symbol, init_zoom_periods=1)
    # fplt.plot(df.index, df.Close, width=1)
    fplt.candlestick_ochl(df[['Open','Close','High','Low']], ax=ax)

    fplt.add_line((xmax, 0), (xmax, 1000000), color='#9900ff', interactive=True)
    fplt.add_line((df.index[1],buy_price), (df.index[-1], buy_price), color='#9900ff', interactive=True)
    fplt.add_line((df.index[1],stop_price), (df.index[-1], stop_price), color='#ff0000', interactive=True)
    fplt.add_line((df.index[1],target_price), (df.index[-1], target_price), color='#00ff00', interactive=True)

    fplt.set_x_pos(xmin, xmax, ax=ax)

    axo = ax.overlay()
    fplt.volume_ocv(df[['Open','Close','Volume']], ax=axo)



    


    fplt.show()

df = md.df_from_csv('./shares and dates.csv')

for date,row in df.iterrows():

    

    date = datetime.datetime.strftime(date,'%Y-%m-%d')

    try:
        plot_specific_dates(symbol=row.Symbol, end_date=date,buy_price=row.Buy_price, stop_price=row.Stop_price, target_price=row.Target_price)

    except:
        print(f'unable to print {row.Symbol}')