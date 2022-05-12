import finplot as fplt
import pandas as pd
import yfinance as yf
import numpy as np
import technical_indicators as ti
import market_data as md

# create a chart where background colours show weekly impulse and also plot daily candles and force index. To be used for Elder Triple Screen

symbol = 'ABF.L'

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