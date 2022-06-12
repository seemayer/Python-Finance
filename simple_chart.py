from audioop import add
from datetime import datetime
import finplot as fplt
import numpy as np
import pandas as pd
import yfinance as yf
import config
import market_data as md
import technical_indicators as ti

def add_volume():
    # overlay volume on the top plot
    volumes = df[['Open','Close','Volume']]
    fplt.volume_ocv(volumes, ax=ax.overlay())

def add_moving_average(period):
    # put an MA on the close price
    ma = df['Close'].rolling(period).mean()
    fplt.plot(ma, ax=ax, legend=f'ma-{period}')

def add_exponential_moving_average(period):
    # put an EMA on the close price
    ti.add_ema(df,period)
    fplt.plot(df[f'{period}EMA'], ax=ax, legend=f'{period}EMA')

def add_macd():
  ti.add_macd(df)
  fplt.volume_ocv(df[['Open','Close','macd_diff']], ax=ax2, colorfunc=fplt.strength_colorfilter)

def add_marker(date, value, style='o',name='mark'):
    
    if not 'marker' in df.columns:
        df['marker'] = np.nan
    # symbols https://www.geeksforgeeks.org/pyqtgraph-symbols/
    df.at[date, 'marker'] = value
    fplt.plot(df['marker'], ax=ax, color='#4a5', style=style, legend=name)

def add_candles():
    # plot candle sticks
    candles = df[['Open','Close','High','Low']]
    fplt.candlestick_ochl(candles, ax=ax)

def add_weekly_impulse(): 
# create a chart where background colours show weekly impulse and also plot daily candles and force index. To be used for Elder Triple Screen

  df_weekly = md.resample_weekly(df)

  ti.add_elder_impulse(df_weekly)
  df_weekly = df_weekly[['Open','Close','impulse']] #Filter columns

  conditions = [
      (df_weekly.impulse.eq('green')), #green
      (df_weekly.impulse.eq('blue')),  #blue
      (df_weekly.impulse.eq('red'))   #red
      ]
  
  # create a list of the values we want to assign for each condition
  open_values = [0, 0, 1000000] #Green, Blue, Red
  close_values = [1000000, 0, 0]
  
  # create a new column and use np.select to assign values to it using our lists as arguments
  df_weekly['Open'] = np.select(conditions, open_values)
  df_weekly['Close'] = np.select(conditions, close_values)
  
  df_weekly = md.resample_daily(df_weekly)
  
  # reduce to original date list to avoid having gaps in data on weekends\bank holidays
  date_list = df.index.to_list()
  df_weekly = df_weekly[df_weekly.index.isin(date_list)] 

  #Create plot with blue background and 2 windows
  
  ax.vb.setBackgroundColor('#87CEEB')

  # plot weekly candles first
  weekly_plot = fplt.candlestick_ochl(df_weekly[['Open','Close']], candle_width=1)
  weekly_plot.colors.update(dict(bull_frame = '#ada', bull_body='#ada', bull_shadow='#ada', bear_body='#fbc', bear_frame='#fbc'))

def add_force_index():
    # add Force Index
    ti.add_force_index(df)
    fplt.volume_ocv(df[['Open','Close','force_index']], ax=ax2, colorfunc=fplt.strength_colorfilter)

def add_hline(value):
    fplt.add_line((df.index[1],value), (df.index[-1], value), color='#9900ff')

def add_vline(date):
    date = pd.to_datetime(date)
    fplt.add_line((date, 0), (date, 1000000), color='#9900ff')

def plot():

    global ax,ax2,df

    symbol='888.L'
    filepath = config.DATA_DIR + symbol + '.csv'

    df = md.get_stock_data(symbol)
    # df = md.df_from_csv(filepath)

    # create two axes
    ax,ax2 = fplt.create_plot(symbol, rows=2)

    # add_weekly_impulse()

    add_candles()
    add_volume()

    add_moving_average(25)
    add_moving_average(50)

    add_exponential_moving_average(10)

    add_marker('2022-06-10', 260)

    add_hline(300)
    add_vline('2022-03-15')

    add_macd()
    # add_force_index(df)

    # we're done
    fplt.show()

if __name__ == "__main__":
    plot()
