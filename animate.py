#!/usr/bin/env python3

import finplot as fplt
import numpy as np
import pandas as pd
import yfinance as yf
import datetime


FPS = 30
anim_counter = 0
spots = None
labels_plot = None

def move_view(ax, df):
    global anim_counter

    xmin = datetime.datetime.strptime('2021-06-01', "%Y-%m-%d").timestamp()
    xmax = datetime.datetime.strptime('2021-07-14', "%Y-%m-%d").timestamp()

    fplt.set_x_pos(xmin, xmax, ax=ax)

    # fplt.set_x_pos(df.index[anim_counter], df.index[anim_counter+100], ax=ax)
    # fplt.set_x_pos(df.index[int(x-w)], df.index[int(x+w)], ax=ax)
    print(f'df.index[anim_counter] = {df.index[anim_counter],type(df.index[anim_counter])}')
    anim_counter += 1


def animate(ax, df):

    move_view(ax, df)


df = yf.download('888.L', period='1y',interval='1d')
print(len(df))
ax = fplt.create_plot('Things move', init_zoom_periods=100, maximize=False)
df.plot(kind='candle', ax=ax)

fplt.timer_callback(lambda: animate(ax, df), 1/FPS)
fplt.show()