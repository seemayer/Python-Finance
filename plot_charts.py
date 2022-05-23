import finplot as fplt
import pandas as pd
import yfinance as yf
import numpy as np
import technical_indicators as ti
import market_data as md
import os
from pathlib import Path
  
def triple_screen(filepath = '.\data\VOD.L.csv'): 

# create a chart where background colours show weekly impulse and also plot daily candles and force index. To be used for Elder Triple Screen
  file = Path(filepath)
  symbol = file.name[:-4]
  interval = '1d'
  
  df = md.df_from_csv(file)
  df_weekly = md.resample_weekly(df)
  # print(df)

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
  df = df.reset_index()
  df['Date'] = pd.to_datetime(df['Date']).view('int64') # convert from object to use finplot's internal representation, which is ns
  df = df.set_index('Date')
  
  fplt.odd_plot_background = '#87CEEB' # blue
  ax,ax2 = fplt.create_plot(symbol, rows=2, maximize=True)
  hover_label = fplt.add_legend('', ax=ax)
  
  # plot weekly candles first
  weekly_plot = fplt.candlestick_ochl(df_weekly[['Open','Close']], candle_width=1)
  weekly_plot.colors.update(dict(bull_frame = '#ada', bull_body='#ada', bull_shadow='#ada', bear_body='#fbc', bear_frame='#fbc'))
  
  # plot daily candles on top
  fplt.candlestick_ochl(df[['Open','Close','High','Low']])
  
  # 13 EMA
  ti.add_ema(df, period = 13)
  fplt.plot(df['13EMA'], ax=ax, legend='13EMA')

  # 26 EMA
  ti.add_ema(df, period = 26)
  fplt.plot(df['26EMA'], ax=ax, legend='26EMA')

  # Autoenvelope
  ti.add_auto_envelope(df)
  fplt.plot(df['upper_channel'], ax=ax, legend='upper_channel')
  fplt.plot(df['lower_channel'], ax=ax, legend='lower_channel')
  
  # add Force Index
  ti.add_force_index(df)
  fplt.volume_ocv(df[['Open','Close','force_index']], ax=ax2, colorfunc=fplt.strength_colorfilter)

  # add Safe Zone
  ti.add_safe_zone_stops(df)
  fplt.plot(df['Downtrend_Buy_Stop'], ax=ax, legend='SafeZone Stop')

  # plot macd
  # ti.add_macd(df)
  # fplt.volume_ocv(df[['Open','Close','macd_diff']], ax=ax2, colorfunc=fplt.strength_colorfilter)

  #######################################################
  ## update crosshair and legend when moving the mouse ##
  
  def update_legend_text(x, y):
      row = df.loc[df.index==x]
      # format html with the candle and set legend
      fmt = '<span style="color:#%s">%%.2f</span>' % ('0b0' if (row.Open<row.Close).all() else 'a00')
      rawtxt = '<span style="font-size:13px">%%s %%s</span> &nbsp; O%s C%s H%s L%s' % (fmt, fmt, fmt, fmt)
      hover_label.setText(rawtxt % (symbol, interval.upper(), row.Open, row.Close, row.High, row.Low))
  
  def update_crosshair_text(x, y, xtext, ytext):
      ytext = '%s (Close%+.2f)' % (ytext, (y - df.iloc[x].Close))
      return xtext, ytext
  
  fplt.set_time_inspector(update_legend_text, ax=ax, when='hover')
  fplt.add_crosshair_info(update_crosshair_text, ax=ax)

  fplt.show()

def plot_chart(symbol, interval):

  df = pd.read_csv('screen passed/' + symbol + '.csv')
  df['Date'] = pd.to_datetime(df['Date']).view('int64') # convert from object to use finplot's internal representation, which is ns
  df = df.set_index('Date')
  
  ax,ax2 = fplt.create_plot(symbol, rows=2)

  # plot macd with standard colors first
  ti.add_macd(df)
  fplt.volume_ocv(df[['Open','Close','macd_diff']], ax=ax2, colorfunc=fplt.strength_colorfilter)
  
  fplt.plot(df.macd, ax=ax2, legend='MACD')
  fplt.plot(df.signal, ax=ax2, legend='Signal')
  
  # plot price and volume
  fplt.candlestick_ochl(df[['Open','Close','High','Low']], ax=ax)
  hover_label = fplt.add_legend('', ax=ax)
  axo = ax.overlay()
  fplt.volume_ocv(df[['Open','Close','Volume']], ax=axo)
  fplt.plot(df.Volume.ewm(span=24).mean(), ax=axo, color=1)
  
  #######################################################
  ## update crosshair and legend when moving the mouse ##
  
  def update_legend_text(x, y):
      row = df.loc[df.index==x]
      # format html with the candle and set legend
      fmt = '<span style="color:#%s">%%.2f</span>' % ('0b0' if (row.Open<row.Close).all() else 'a00')
      rawtxt = '<span style="font-size:13px">%%s %%s</span> &nbsp; O%s C%s H%s L%s' % (fmt, fmt, fmt, fmt)
      hover_label.setText(rawtxt % (symbol, interval.upper(), row.Open, row.Close, row.High, row.Low))
  
  def update_crosshair_text(x, y, xtext, ytext):
      ytext = '%s (Close%+.2f)' % (ytext, (y - df.iloc[x].Close))
      return xtext, ytext
  
  fplt.set_time_inspector(update_legend_text, ax=ax, when='hover')
  fplt.add_crosshair_info(update_crosshair_text, ax=ax)
  
  # fplt.plot(df['marker'], ax=ax, color='#4a5', style='^', legend='dumb mark')

  fplt.show()

def screen_passed():
  for file in os.scandir('./screen passed/'):
    name = file.name[:-4] 
    print(name)
  
    try:
      triple_screen(file)
    except:
      print('unable to plot '+ name)


if __name__ == "__main__":
  # stuff only to run when not called via 'import' here
  screen_passed()
  # triple_screen()
  # plot_chart('888.L','1d')