#https://github.com/highfestiva/finplot/wiki/Examples#featured-example

#!/usr/bin/env python3

import finplot as fplt
import pandas as pd
import requests
from io import StringIO
from time import time

def plot_chart(file):

  df = pd.read_csv('data/GOOG.csv', index_col = False)
  
  df['Date'] = pd.to_datetime(df['Date']).view('int64') # use finplot's internal representation, which is ns
  print(df.tail(6))
  
  ax,ax2 = fplt.create_plot('TITLE', rows=2)
  
  # plot macd with standard colors first
  fplt.volume_ocv(df[['Date','Open','Close','macd_diff']], ax=ax2, colorfunc=fplt.strength_colorfilter)
  fplt.plot(df.macd, ax=ax2, legend='MACD')
  fplt.plot(df.signal, ax=ax2, legend='Signal')
  
  # plot price and volume
  #fplt.candlestick_ochl(df[['Date','Open','Close','High','Low']], ax=ax)
  #hover_label = fplt.add_legend('', ax=ax)
  #axo = ax.overlay()
  #fplt.volume_ocv(df[['Date','Open','Close','Volume']], ax=axo)
  #fplt.plot(df.Volume.ewm(span=24).mean(), ax=axo, color=1)
  
  #######################################################
  ## update crosshair and legend when moving the mouse ##
  
  #def update_legend_text(x, y):
      #row = df.loc[df.Date==x]
      # format html with the candle and set legend
      #fmt = '<span style="color:#%s">%%.2f</span>' % ('0b0' if (row.Open<row.Close).all() else 'a00')
      #rawtxt = '<span style="font-size:13px">%%s %%s</span> &nbsp; O%s C%s H%s L%s' % (fmt, fmt, fmt, fmt)
      #hover_label.setText(rawtxt % (symbol, interval.upper(), row.Open, row.Close, row.High, row.Low))
  
  #def update_crosshair_text(x, y, xtext, ytext):
      #ytext = '%s (Close%+.2f)' % (ytext, (y - df.iloc[x].Close))
      #return xtext, ytext
  
  #fplt.set_time_inspector(update_legend_text, ax=ax, when='hover')
  #fplt.add_crosshair_info(update_crosshair_text, ax=ax)
  
  fplt.show()