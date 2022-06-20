import finplot as fplt
import os
import numpy as np
import market_data as md
import pandas as pd
import technical_indicators as ti
from datetime import datetime
import pprint as pp

class myplot():

    def create(self, symbol='TEST', init_zoom_periods=1e10):
        self.ax, self.ax2 = fplt.create_plot(symbol, rows=2, init_zoom_periods=init_zoom_periods)

    def show(self):
        fplt.show()

    def add_candles(self, main_df):
        df = main_df.copy()
        # plot candle sticks
        candles = df[['Open','Close','High','Low']]
        fplt.candlestick_ochl(candles, ax=self.ax)

    def add_volume(self, main_df):
        df = main_df.copy()
        # overlay volume on the top plot
        volumes = df[['Open','Close','Volume']]
        fplt.volume_ocv(volumes, ax=self.ax.overlay())

    def add_moving_average(self, main_df, period):
        df = main_df.copy()
        # put an MA on the close price
        ma = df['Close'].rolling(period).mean()
        fplt.plot(ma, ax=self.ax, legend=f'MA-{period}')

    def add_exponential_moving_average(self, main_df, period):
        df = main_df.copy()
        # put an EMA on the close price
        df = ti.add_ema(df,period)
        fplt.plot(df[f'EMA-{period}'], ax=self.ax, legend=f'EMA-{period}')

    def add_ATR_fan(self, main_df, period):
        df = main_df.copy()
        # put an EMA on the close price
        df = ti.add_avg_true_range(df,period)
        fplt.plot(df[f'EMA-{period}'], ax=self.ax, legend=f'EMA-{period}')


    def add_macd(self, main_df):
        df = main_df.copy()
        df = ti.add_macd(df)
        fplt.volume_ocv(df[['Open','Close','macd_diff']], ax=self.ax2, colorfunc=fplt.strength_colorfilter)

    def add_marker(self, main_df, date, value, style='o',name='mark',color='blue'):
        df = main_df.copy()
        if not 'marker' in df.columns:
            df['marker'] = np.nan
        # symbols https://www.geeksforgeeks.org/pyqtgraph-symbols/
        df.at[date, 'marker'] = value
        fplt.plot(df['marker'], ax=self.ax, color=color, style=style, legend=name)

    def add_weekly_impulse(self, main_df): 
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
        self.ax.vb.setBackgroundColor('#87CEEB')

        weekly_plot = fplt.candlestick_ochl(df_weekly[['Open','Close']], candle_width=1)
        weekly_plot.colors.update(dict(bull_frame = '#ada', bull_body='#ada', bull_shadow='#ada', bear_body='#fbc', bear_frame='#fbc'))        # plot weekly candles first

    def add_force_index(self, main_df):
        df = main_df.copy()
        # add Force Index
        df = ti.add_force_index(df)
        fplt.volume_ocv(df[['Open','Close','force_index']], ax=self.ax2, colorfunc=fplt.strength_colorfilter)

    def add_hline(self, main_df,value, start_date=None, length=5, width=1, color='blue'):
        df = main_df.copy()

        if start_date != None:
            i2 = df.index.get_loc(start_date)
            i1 = min(max(i2 + length,0),len(df.index)-1)
        else:
            i2 = -1
            i1 = 0

        fplt.add_line((df.index[i1],value), (df.index[i2], value), color=color, width=width)

    def add_vline(self, date, color='green', width=1):
        date = pd.to_datetime(date)
        fplt.add_line((date, 0), (date, 1000000), color=color,width=width)

    def add_auto_envelope(self, main_df):
        df = main_df.copy()
        df = ti.add_auto_envelope(df)
        fplt.plot(df['upper_channel'], ax=self.ax, legend='upper_channel')
        fplt.plot(df['lower_channel'], ax=self.ax, legend='lower_channel')

    def add_safe_zone_stops(self, main_df):
        df = main_df.copy()
        df = ti.add_safe_zone_stops(df)
        fplt.plot(df['Downtrend_Buy_Stop'], ax=self.ax, legend='SafeZone Stop')
        fplt.plot(df['Uptrend_Sell_Stop'], ax=self.ax, legend='SafeZone Stop')

    def plot_specific_dates(self, start_date='2021-05-01', end_date='2021-07-25'):

        # need to make sure dates are within the data range
        xmin = datetime.strptime(start_date, "%Y-%m-%d").timestamp()
        xmax = datetime.strptime(end_date, "%Y-%m-%d").timestamp()

        fplt.set_x_pos(xmin, xmax, ax=self.ax)

#   #######################################################
#   ## update crosshair and legend when moving the mouse ##
  
#   def update_legend_text(x, y):
#       row = df.loc[pd.to_datetime(df.index).view('int64')==x]
#       # format html with the candle and set legend
#       fmt = '<span style="color:#%s">%%.2f</span>' % ('0b0' if (row.Open<row.Close).all() else 'a00')
#       rawtxt = '<span style="font-size:13px">%%s %%s</span> &nbsp; O%s C%s H%s L%s' % (fmt, fmt, fmt, fmt)
#       hover_label.setText(rawtxt % ('TEST', '1D', row.Open, row.Close, row.High, row.Low))
  
#   def update_crosshair_text(x, y, xtext, ytext):
#       ytext = '%s (Close%+.2f)' % (ytext, (y - df.iloc[x].Close))
#       return xtext, ytext
  
#   fplt.set_time_inspector(update_legend_text, ax=ax, when='hover')
#   fplt.add_crosshair_info(update_crosshair_text, ax=ax)

############### PLOT TYPES #####################

def triple_screen_plot(df, symbol): 
    plt = myplot()
    plt.create(symbol=symbol)

    # create a chart where background colours show weekly impulse and also plot daily candles and force index. To be used for Elder Triple Screen
    plt.add_weekly_impulse(df)
    plt.add_candles(df)
    plt.add_exponential_moving_average(df,13)
    plt.add_exponential_moving_average(df,26)
    plt.add_auto_envelope(df)
    plt.add_force_index(df)
    plt.add_safe_zone_stops(df)
    plt.show()

def standard_plot(df, symbol=None):
    plt = myplot()
    plt.create(symbol=symbol)
    plt.add_candles(df)
    plt.add_volume(df)
    plt.add_moving_average(df, period=13)
    plt.add_exponential_moving_average(df, period=200)
    plt.add_macd(df)
    plt.show() 

def screen_passed(plot_type=standard_plot):
    for file in os.scandir('./screen passed/'):
        name = file.name[:-4] 
        print(name)
        try:
            df = md.df_from_csv(file.path)
            plot_type(df, name) #plot type passed as function
            # standard_plot(df, name)
            # triple_screen_plot(df, name)
        except:
            print('unable to plot '+ name)

if __name__ == "__main__": 

    screen_passed()
    # screen_passed(standard_plot)
    # screen_passed(triple_screen_plot)
    
    # df = md.df_from_csv('./data/888.L.csv')

    # plt = myplot()

    # plt.create(symbol='EPIC')
    # plt.add_weekly_impulse(df) #must be run before plot candles
    # plt.add_candles(df)
    # plt.add_volume(df)
    # plt.add_moving_average(df, period=13)
    # plt.add_exponential_moving_average(df, period=200)
    # plt.add_macd(df)
    # plt.add_marker(df, date='2022-03-03', value=260, style='o',name='mark',color='blue')
    # plt.add_force_index(df)
    # plt.add_hline(df,value=230, start_date='2022-02-03', length=500, color='pink',width=5)
    # plt.add_vline(date='2022-02-03',color='yellow',width=10)
    # plt.add_auto_envelope(df)
    # plt.add_safe_zone_stops(df)
    # plt.plot_specific_dates(start_date='2021-05-01', end_date='2021-07-25')
    # plt.show()

