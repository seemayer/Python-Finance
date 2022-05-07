#!/usr/bin/env python3

from datetime import date, timedelta
import finplot as fplt
import pandas as pd
import yfinance as yf
import numpy as np
import add_indicators as ai

def resample_weekly(df):

    # resample to weekly candles, i.e. five 1-day candles per business week
    dfw = df.Open.resample('W').first().to_frame()
    dfw['Close'] = df.Close.resample('W').last()
    dfw['High'] = df.High.resample('W').max()
    dfw['Low'] = df.Low.resample('W').min()
    dfw['Volume'] = df.Volume.resample('W').sum()

    dfw = dfw.dropna()

    return dfw

def plot_chart(df):

    df = df.reset_index(level=0)

    period = 22
    # add EMA of length period
    df[str(period) + 'EMA'] = df.Close.ewm(span=period).mean()

    # add MACD, Signal and histogram (diff)
    df['macd'] = df.Close.ewm(span=12).mean() - df.Close.ewm(span=26).mean()
    df['signal'] = df.macd.ewm(span=9).mean()
    df['macd_diff'] = df.macd - df.signal

    df['Date'] = pd.to_datetime(df['Date']).view('int64') # use finplot's internal representation, which is ns
    print(df.tail(6))
  
    ax,ax2 = fplt.create_plot('TITLE', rows=2)
    
    # plot macd with standard colors first
    fplt.volume_ocv(df[['Date','Open','Close','macd_diff']], ax=ax2, colorfunc=fplt.strength_colorfilter)
    fplt.plot(df.macd, ax=ax2, legend='MACD')
    fplt.plot(df.signal, ax=ax2, legend='Signal')

    # plot price and volume
    fplt.candlestick_ochl(df[['Date','Open','Close','High','Low']], ax=ax)
    fplt.plot(df['Date'], df['Close'].ewm(span=25).mean(), ax=ax, legend='ema-25')
    fplt.plot(df['Date'], df['Close'].rolling(25).mean(), ax=ax, legend='sma-25')
    # hover_label = fplt.add_legend('', ax=ax)
    axo = ax.overlay()
    fplt.volume_ocv(df[['Date','Open','Close','Volume']], ax=axo)
    fplt.plot(df.Volume.ewm(span=24).mean(), ax=axo, color=1)

    fplt.show()

#get daily data
df = yf.download('GOOG', period='2y', interval='1d')

#convert to weekly data
dfw = resample_weekly(df)


# when writing and reading back from csv the index is convert to an object type so need to convert back to datetime64
dfw.to_csv("./TEST.csv", sep=',')
dfw = pd.read_csv('./TEST.csv')
dfw['Date'] = pd.to_datetime(dfw['Date'])
dfw = dfw.set_index('Date')






#Create copy of weekly data for shading
dfwshade = dfw[['Open','Close']].copy()

# dfw = dfw.reset_index(level=0)
# dfw['Date'] = pd.to_datetime(dfw['Date']).view('int64') # use finplot's internal representation, which is ns

ai.elder_impulse(dfwshade)
dfwshade = dfwshade[['Open','Close','impulse']]
print(dfwshade)

# plot_chart(df)

# plot_chart(dfw)

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
fplt.odd_plot_background = '#87CEEB' # yellow
# fplt.odd_plot_background = '#f0f' # purple

ax,ax2 = fplt.create_plot('TITLE', rows=2, maximize=True)

# plot down-sampled weekly candles first

weekly_plot = fplt.candlestick_ochl(dfwshade[['Open','Close']], candle_width=1)
weekly_plot.colors.update(dict(bull_frame = '#ada', bull_body='#ada', bull_shadow='#ada', bear_body='#fbc', bear_frame='#fbc'))

# plot daily candles on top & 22 EMA
fplt.candlestick_ochl(dfw[['Open','Close','High','Low']])
fplt.plot(dfw['Close'].ewm(span=22).mean(), ax=ax, legend='ema-22')

# add MACD, Signal and histogram (diff)
dfw['macd'] = dfw.Close.ewm(span=12).mean() - dfw.Close.ewm(span=26).mean()
dfw['signal'] = dfw.macd.ewm(span=9).mean()
dfw['macd_diff'] = dfw.macd - dfw.signal



# plot macd with standard colors first
fplt.volume_ocv(dfw[['Open','Close','macd_diff']], ax=ax2, colorfunc=fplt.strength_colorfilter)
fplt.plot(dfw.macd, ax=ax2, legend='MACD')
fplt.plot(dfw.signal, ax=ax2, legend='Signal')

fplt.show()