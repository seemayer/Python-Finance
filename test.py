#!/usr/bin/env python3

import finplot as fplt
import yfinance as yf
import datetime

df = yf.download('888.L', period='5y',interval='1d')

xmin = datetime.datetime.strptime('2021-06-01', "%Y-%m-%d").timestamp()
xmax = datetime.datetime.strptime('2021-06-12', "%Y-%m-%d").timestamp()

ax = fplt.create_plot('Things move', init_zoom_periods=1)
fplt.candlestick_ochl(df[['Open','Close','High','Low']], ax=ax)

fplt.set_x_pos(xmin, xmax, ax=ax)

fplt.show()

