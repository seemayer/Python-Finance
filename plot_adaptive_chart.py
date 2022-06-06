#!/usr/bin/env python3
'''A lengthy example that shows some more complex uses of finplot:
    - control panel in PyQt
    - varying indicators, intervals and layout
    - toggle dark mode
    - price line
    - real-time updates via websocket

   This example includes dipping in to the internals of finplot and
   the underlying lib pyqtgraph, which is not part of the API per se,
   and may thus change in the future. If so happens, this example
   will be updated to reflect such changes.

   Included is also some third-party libraries to make the example
   more realistic.
   '''

import finplot as fplt
from PyQt5.QtWidgets import QComboBox, QCheckBox, QWidget, QGridLayout
import pyqtgraph as pg
import pandas as pd
import config

def calc_plot_data(df, mafan_checked, MACD_checked):
    '''Returns data for all plots and for the price line.'''
    price = df['Open Close High Low'.split()]
    volume = df['Open Close Volume'.split()]
    mafan = macd = signal = macd_data = None

    if mafan_checked:
        mafan = pd.DataFrame({
            'ema8': price.Close.ewm(span=8).mean(),
            'ema20': price.Close.ewm(span=20).mean(),
            'ema50': price.Close.ewm(span=50).mean(),
            'ema100': price.Close.ewm(span=100).mean(),
            'ema150': price.Close.ewm(span=150).mean(),
            'ema200': price.Close.ewm(span=200).mean(),
            'ma200' : price.Close.rolling(200).mean()
            })
    if MACD_checked:
        macd = price.Close.ewm(span=12).mean() - price.Close.ewm(span=26).mean()
        signal = macd.ewm(span=9).mean()
        
        macd_data = pd.DataFrame({
            'Open' : df.Open,
            'Close' : df.Close,
            'macd_diff' : macd - signal
        })
        
    plot_data = dict(price=price, volume=volume, mafan=mafan, macd=macd, signal=signal, macd_data=macd_data)

    return plot_data

def load_price_history(symbol):
   
    df = pd.read_csv(config.DATA_DIR + symbol + '.csv')
    df['Date'] = pd.to_datetime(df['Date']).view('int64') # convert from object to use finplot's internal representation, which is ns
    df = df.set_index('Date')   

    return df

def change_asset(*args, **kwargs):
    '''Resets and recalculates everything, and plots for the first time.'''
    # save window zoom position before resetting
    fplt._savewindata(fplt.windows[0])

    symbol = ctrl_panel.symbol.currentText()

    df = load_price_history(symbol)

    # remove any previous plots
    ax.reset()
    axo.reset()
    ax_macd.reset()

    # calculate plot data
    # indicators = ctrl_panel.indicators.currentText().lower()
    mafan_chk = ctrl_panel.mafan.isChecked()
    macd_chk = ctrl_panel.MACD.isChecked()
    data = calc_plot_data(df, mafan_chk, macd_chk)

    # some space for legend
    ctrl_panel.move(200, 0)

    # plot data
    global plots
    plots = {}
    plots['price'] = fplt.candlestick_ochl(data['price'], ax=ax)
    plots['volume'] = fplt.volume_ocv(data['volume'], ax=axo)
    
    if data['mafan'] is not None:
        for colName,colData in data['mafan'].iteritems():
            plots[colName] = fplt.plot(colData, legend=colName, ax=ax)
    if ctrl_panel.MACD.isChecked():
        ax_macd.show()
        plots['macd'] = fplt.plot(data['macd'], color=4, legend='MACD', ax=ax_macd)
        plots['signal'] = fplt.plot(data['signal'], color=4, legend='Signal', ax=ax_macd)
        plots['macd_data'] = fplt.volume_ocv(data['macd_data'], ax=ax_macd, colorfunc=fplt.strength_colorfilter)
    else:
        ax.set_visible(xaxis=True)
        ax_macd.hide()

    # restores saved zoom position, if in range
    fplt.refresh()


def create_ctrl_panel(win):
    
    panel = QWidget(win)
    panel.move(100, 0)
    win.scene().addWidget(panel)
    layout = QGridLayout(panel)

    panel.symbol = QComboBox(panel)
    [panel.symbol.addItem(i+'.L') for i in '888 AAF ADM AEP AMGO APP'.split()]
    panel.symbol.setCurrentIndex(1)
    layout.addWidget(panel.symbol, 0, 0)
    panel.symbol.currentTextChanged.connect(change_asset)

    panel.mafan = QCheckBox(panel)
    panel.mafan.setText('MA Fan')
    panel.mafan.setCheckState(2)
    panel.mafan.toggled.connect(change_asset)
    layout.addWidget(panel.mafan, 0, 1)

    panel.MACD = QCheckBox(panel)
    panel.MACD.setText('MACD')
    panel.MACD.setCheckState(2)
    panel.MACD.toggled.connect(change_asset)
    layout.addWidget(panel.MACD, 0, 2)

    return panel

plots = {}
fplt.y_pad = 0.07 # pad some extra (for control panel)
fplt.max_zoom_points = 7
fplt.autoviewrestore()
ax,ax_macd = fplt.create_plot('Adaptive Chart', rows=2, init_zoom_periods=300)
axo = ax.overlay()

# hide rsi chart to begin with; show x-axis of top plot
# ax_rsi.hide()
ax_macd.vb.setBackgroundColor(None) # don't use odd background color
ax.set_visible(xaxis=True)

ctrl_panel = create_ctrl_panel(ax.vb.win)
change_asset()
# fplt.timer_callback(realtime_update_plot, 1) # update every second
fplt.show()
