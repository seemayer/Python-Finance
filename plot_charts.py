import finplot as fplt
import pandas as pd
import yfinance as yf
import numpy as np
import technical_indicators as ti
import market_data as md
import os
  
def triple_screen(symbol = 'GOOG'): 

# create a chart where background colours show weekly impulse and also plot daily candles and force index. To be used for Elder Triple Screen
  
  df = md.get_stock_data(symbol, period='2y')
  
  #convert to weekly data
  dfw = md.resample_weekly(df)
  
  #Create copy of weekly data for shading
  dfwshade = dfw[['Open','Close']].copy()
  
  ti.add_elder_impulse(dfwshade)
  dfwshade = dfwshade[['Open','Close','impulse']]
  print(dfwshade)
  
  conditions = [
      (dfwshade.impulse.eq('green')), #green
      (dfwshade.impulse.eq('blue')),  #blue
      (dfwshade.impulse.eq('red'))   #red
      ]
  
  # create a list of the values we want to assign for each condition
  open_values = [0, 0, 1000000]
  close_values = [1000000,0, 0]
  
  # create a new column and use np.select to assign values to it using our lists as arguments
  dfwshade['Open'] = np.select(conditions, open_values)
  dfwshade['Close'] = np.select(conditions, close_values)
  
  #Create plot with blue background and 2 windows
  fplt.odd_plot_background = '#87CEEB' # blue
  
  ax,ax2 = fplt.create_plot('TITLE', rows=2, maximize=True)
  
  hover_label = fplt.add_legend('', ax=ax)
  axo = ax.overlay()
  
  
  # plot down-sampled weekly candles first
  weekly_plot = fplt.candlestick_ochl(dfwshade[['Open','Close']], candle_width=5)
  weekly_plot.colors.update(dict(bull_frame = '#ada', bull_body='#ada', bull_shadow='#ada', bear_body='#fbc', bear_frame='#fbc'))
  weekly_plot.x_offset = 2.1 # resample() gets us start of day, offset +1.1 (gap+off center wick)
  
  # plot daily candles on top & 13 EMA
  fplt.candlestick_ochl(df[['Open','Close','High','Low']])
  fplt.plot(df['Close'].ewm(span=13).mean(), ax=ax, legend='ema-13')
  
  # add Force Index
  ti.add_force_index(df)
  
  # plot force index
  # fplt.plot(df.force_index, ax=ax2, legend='Force Index')
  fplt.volume_ocv(df[['Open','Close','force_index']], ax=ax2, colorfunc=fplt.strength_colorfilter)
  
  fplt.show()




def plot_chart(symbol, interval):

  df = pd.read_csv('screen passed/' + symbol + '.csv')
  df['Date'] = pd.to_datetime(df['Date']).view('int64') # convert from object to use finplot's internal representation, which is ns
  df = df.set_index('Date')
  
  # fplt.candle_bull_color = '#C0FF3E'
  # fplt.candle_bull_body_color = '#C0FF3E'
  # fplt.candle_bear_color = '#0000FF'
  # fplt.candle_shadow_width = 1
  
  ax,ax2 = fplt.create_plot(symbol, rows=2)
  

  # plot macd with standard colors first
  ti.macd(df)
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

# plot_chart('AAF.L','1d')


def screen_passed():
  for file in os.scandir('./screen passed/'):
    name = file.name[:-4] 
    print(name)
  
    try:
      plot_chart(name,'1d')
    except:
      print('unable to plot '+ name)