from audioop import add
from datetime import datetime
import finplot as fplt
import numpy as np
import pandas as pd
import yfinance as yf
import config
import market_data as md
import technical_indicators as ti
from pathlib import Path
import os

def add_volume(main_df):
    df = main_df.copy()
    # overlay volume on the top plot
    volumes = df[['Open','Close','Volume']]
    fplt.volume_ocv(volumes, ax=ax.overlay())

def add_moving_average(main_df, period):
    df = main_df.copy()
    # put an MA on the close price
    ma = df['Close'].rolling(period).mean()
    fplt.plot(ma, ax=ax, legend=f'MA-{period}')

def add_exponential_moving_average(main_df, period):
    df = main_df.copy()
    # put an EMA on the close price
    df = ti.add_ema(df,period)
    fplt.plot(df[f'EMA-{period}'], ax=ax, legend=f'EMA-{period}')

def add_macd(main_df):
  df = main_df.copy()
  df = ti.add_macd(df)
  fplt.volume_ocv(df[['Open','Close','macd_diff']], ax=ax2, colorfunc=fplt.strength_colorfilter)

def add_marker(main_df, date, value, style='o',name='mark'):
    df = main_df.copy()
    if not 'marker' in df.columns:
        df['marker'] = np.nan
    # symbols https://www.geeksforgeeks.org/pyqtgraph-symbols/
    df.at[date, 'marker'] = value
    fplt.plot(df['marker'], ax=ax, color='#4a5', style=style, legend=name)

def add_candles(main_df):
    df = main_df.copy()
    # plot candle sticks
    candles = df[['Open','Close','High','Low']]
    fplt.candlestick_ochl(candles, ax=ax)

def add_weekly_impulse(main_df): 
# create a chart where background colours show weekly impulse and also plot daily candles and force index. To be used for Elder Triple Screen
  df = main_df.copy()
  df_weekly = md.resample_weekly(df)

  df_weekly = ti.add_elder_impulse(df_weekly)
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

def add_force_index(main_df):
    df = main_df.copy()
    # add Force Index
    df = ti.add_force_index(df)
    fplt.volume_ocv(df[['Open','Close','force_index']], ax=ax2, colorfunc=fplt.strength_colorfilter)

def add_hline(main_df,value):
    df = main_df.copy()
    fplt.add_line((df.index[1],value), (df.index[-1], value), color='#9900ff')

def add_vline(date):
    date = pd.to_datetime(date)
    fplt.add_line((date, 0), (date, 1000000), color='#9900ff')

def add_auto_envelope(main_df):
    df = main_df.copy()
    df = ti.add_auto_envelope(df)
    fplt.plot(df['upper_channel'], ax=ax, legend='upper_channel')
    fplt.plot(df['lower_channel'], ax=ax, legend='lower_channel')

def add_safe_zone_stops(main_df):
  df = main_df.copy()
  df = ti.add_safe_zone_stops(df)
  fplt.plot(df['Downtrend_Buy_Stop'], ax=ax, legend='SafeZone Stop')

def plot_specific_dates(start_date='2021-05-01', end_date='2021-07-25'):

    # need to make sure dates are within the data range
    xmin = datetime.strptime(start_date, "%Y-%m-%d").timestamp()
    xmax = datetime.strptime(end_date, "%Y-%m-%d").timestamp()

    fplt.set_x_pos(xmin, xmax, ax=ax)

## plot examples ##
def plot(main_df, symbol):
    df = main_df.copy()

    global ax,ax2
    ax,ax2 = fplt.create_plot(symbol, rows=2,init_zoom_periods=1)
    # hover_label = fplt.add_legend('', ax=ax)

    # add_weekly_impulse(df)

    add_candles(df)
    add_volume(df)

    add_moving_average(df,25)
    add_moving_average(df,50)

    add_exponential_moving_average(df,10)

    add_marker(df,'2022-06-10', 260)

    add_hline(df,300)
    add_vline('2022-03-15')

    add_macd(df)
    add_force_index(df)

    plot_specific_dates()

    # we're done
    fplt.show()

def triple_screen(main_df, symbol): 
  df = main_df.copy()

  global ax,ax2
  ax,ax2 = fplt.create_plot(symbol, rows=2)
  hover_label = fplt.add_legend('', ax=ax)

# create a chart where background colours show weekly impulse and also plot daily candles and force index. To be used for Elder Triple Screen
  add_weekly_impulse(df)
  add_candles(df)
  add_exponential_moving_average(df,13)
  add_exponential_moving_average(df,26)
  add_auto_envelope(df)
  add_force_index(df)
  add_safe_zone_stops(df)

  #######################################################
  ## update crosshair and legend when moving the mouse ##
  
  def update_legend_text(x, y):
      row = df.loc[pd.to_datetime(df.index).view('int64')==x]
      # format html with the candle and set legend
      fmt = '<span style="color:#%s">%%.2f</span>' % ('0b0' if (row.Open<row.Close).all() else 'a00')
      rawtxt = '<span style="font-size:13px">%%s %%s</span> &nbsp; O%s C%s H%s L%s' % (fmt, fmt, fmt, fmt)
      hover_label.setText(rawtxt % ('TEST', '1D', row.Open, row.Close, row.High, row.Low))
  
  def update_crosshair_text(x, y, xtext, ytext):
      ytext = '%s (Close%+.2f)' % (ytext, (y - df.iloc[x].Close))
      return xtext, ytext
  
  fplt.set_time_inspector(update_legend_text, ax=ax, when='hover')
  fplt.add_crosshair_info(update_crosshair_text, ax=ax)

  fplt.show()

def screen_passed():
  for file in os.scandir('./screen passed/'):
    name = file.name[:-4] 
    print(name)
    try:
      df = md.df_from_csv(file.path)
    #   triple_screen(df, name)
      plot(df, name)
    except:
      print('unable to plot '+ name)

if __name__ == "__main__":
    
    filepath = '.\data\VOD.L.csv'
    file = Path(filepath)
    symbol = file.name[:-4]
    interval = '1d'
    period = '2y'
  
    df = yf.download(symbol, interval=interval, period=period)
    # df = md.df_from_csv(filepath)

    # # triple_screen(df)
    plot(df,symbol)
    # screen_passed()
    
    # test()
