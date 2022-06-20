#https://github.com/highfestiva/finplot/blob/master/finplot/examples/analyze.py

# This module will take a dataframe and add specific indicators to that dataframe

import pandas as pd
import numpy as np
import market_data as md
import config

### Dataframe functions ###

def add_ema(main_df, period=13):
    # add EMA of length period
    df = main_df.copy()
    # use SMA as starting amount for EMA
    sma = df.Close.rolling(window=period, min_periods=period).mean()[:period]
    rest = df.Close[period:]
    df[f'EMA-{period}']=pd.concat([sma, rest]).ewm(span=period, adjust=False).mean()
    
    # df[f'{period}EMA'] = df.Close.ewm(span=period).mean()
    return df

def add_force_index(main_df, period=2):
    df = main_df.copy()
    df['force_index'] = df.Close.diff() * df.Volume
    df['force_index'] = df['force_index'].ewm(span=period).mean()
    return df

def add_macd(main_df):
    df = main_df.copy()
    # add MACD, Signal and histogram (diff)
    df['macd'] = df.Close.ewm(span=12).mean() - df.Close.ewm(span=26).mean()
    df['signal'] = df.macd.ewm(span=9).mean()
    df['macd_diff'] = df.macd - df.signal
    return df

def add_macd_cross(main_df):
    df = main_df.copy()  # do not alter original object
    df = add_macd(main_df)
    df['crossover'] = np.sign(df.macd_diff).diff().gt(0)
    df['crossunder'] = np.sign(df.macd_diff).diff().lt(0)
    return df

def add_elder_impulse(main_df, period=13):
    df = main_df.copy()
    df = add_macd(df)  #requires macd columns to be added to df
    df = add_ema(df, period)  #requires ema

    #https://www.dataquest.io/blog/tutorial-add-column-pandas-dataframe-based-on-if-else-condition/
    # create a list of our conditions
    conditions = [
        (df.macd_diff.diff().gt(0) & df[f'EMA-{period}'].diff().gt(0)),  #green
        (df.macd_diff.diff().lt(0) & df[f'EMA-{period}'].diff().lt(0)),  #red
        (df.macd_diff.diff().gt(0) & df[f'EMA-{period}'].diff().lt(0)),  #blue
        (df.macd_diff.diff().lt(0) & df[f'EMA-{period}'].diff().gt(0))  #blue
    ]

    # create a list of the values we want to assign for each condition
    values = ['green', 'red', 'blue', 'blue']

    # create a new column and use np.select to assign values to it using our lists as arguments
    df['impulse'] = np.select(conditions, values)
    return df

def add_weekly_elder_impulse(main_df):

    df = main_df.copy()
    df_weekly = md.resample_weekly(df)
  
    #calculate indicators for each ticker and add to dataframe
    df_weekly = add_elder_impulse(df_weekly)
    df = md.resample_daily(df_weekly)

    return df

def add_elder_bull_divergence(main_df, period=40):
    df = main_df.copy()
    #requires macd columns to be added to df
    df = add_macd(df)
    df = add_macd_cross(df)

    df['lowest_MACD'] = df.macd_diff.rolling(period).min()
    df['MACD_ratio'] = (df.macd_diff / df.lowest_MACD).where(
        df.macd_diff.lt(0), 0)  #ratio of current MACD to lowest
    df['lowest_Low'] = df.Low.rolling(period).min()
    df['MACD_up'] = np.sign(df.macd_diff.diff()).gt(
        0)  #did the MACD hist tick upwards

    # // Bullish divergence

    df.at[df.index[0], ['state']] = '|0,0,0,0|'  # set first item to zero state

    # get location of columns used in below loop based on name
    istate = df.columns.get_loc('state')
    imacd_diff = df.columns.get_loc('macd_diff')
    ilowest_MACD = df.columns.get_loc('lowest_MACD')
    icrossunder = df.columns.get_loc('crossunder')
    iLow = df.columns.get_loc('Low')
    ilowest_Low = df.columns.get_loc('lowest_Low')
    iMACD_ratio = df.columns.get_loc('MACD_ratio')
    iMACD_up = df.columns.get_loc('MACD_up')

    for i in range(1, len(df)):

        newstate = df.iloc[
            i - 1, istate]  # default next state is the same as prior state
        # if divergence triggered on last iteration then reset the state
        if (newstate == '|0,0,0,1|'):
            newstate = '|1,0,0,0|'

        # if todays MACD is the lowest in the last 'nodays' days then trigger condition 1 and reset other conditions
        if (df.iloc[i, imacd_diff] == df.iloc[i, ilowest_MACD]):
            newstate = '|1,0,0,0|'

        # if condition 1 has been triggered (in a prior period) then if MACD crosses below zero then trigger condition 2
        if ((newstate == '|1,0,0,0|') & (df.iloc[i, icrossunder] == True)):
            newstate = '|0,1,0,0|'

        # if both condition 1 & 2 have been triggered in order (in a prior period) then if price hits new lows then trigger condition 3
        if ((newstate == '|0,1,0,0|') &
            (df.iloc[i, iLow] == df.iloc[i, ilowest_Low])):
            newstate = '|0,0,1,0|'
            if (
                    df.iloc[i, iMACD_ratio] > 0.5
            ):  # reset state if second MACD low is too big (>50% of prior low)
                newstate = '|0,0,0,0|'

        # if conditions 1, 2 & 3 have been triggered in that order then check if the MACD ticks upwards and issue a signal if so
        if ((newstate == '|0,0,1,0|') & (df.iloc[i, iMACD_up] == True) &
            (df.iloc[i, iMACD_ratio] < 0.5)):
            newstate = '|0,0,0,1|'

        df.iat[i, istate] = newstate

    # for plotting purposes capture the low when a divergece is triggered, plot 5 points below it
    df['divergence'] = df['state'] == '|0,0,0,1|'
    df['marker'] = np.where(df['divergence'], df.Low - 5, np.NaN)

    return df

def add_avg_true_range(main_df, period=22):
    df = main_df.copy()
    df['tr1'] = df["High"] - df["Low"]
    df['tr2'] = abs(df["High"] - df["Close"].shift(1))
    df['tr3'] = abs(df["Low"] - df["Close"].shift(1))

    df['true_range'] = df[['tr1', 'tr2', 'tr3']].max(axis=1)
    df['Avg TR'] = df['true_range'].rolling(min_periods=period,
                                            window=period,
                                            center=False).mean()

    # print(df)
    return df

def add_auto_envelope(main_df, ema_period=26, multiplier=2, lookback_period=100):
    df = main_df.copy()
    df = add_ema(df, ema_period)  #requires ema
    df['myvar_squared'] = (df.Close - df[f'EMA-{ema_period}'])**2
    df['mymov'] = df.myvar_squared.rolling(window = lookback_period).mean()**.5
    df['newmax'] = df.mymov.rolling(window=6).max()

    df['upper_channel'] = df[f'EMA-{ema_period}'] + df.newmax*multiplier
    df['lower_channel'] = df[f'EMA-{ema_period}'] - df.newmax*multiplier

    df = df.drop(columns=['myvar_squared',
                     'mymov',
                     'newmax'
                     ])

    return df

def add_safe_zone_stops(main_df, multiplier = 2, window = 10):
    df = main_df.copy()
    
    # for uptrends
    df['Uptrend_Down_Pen'] = -df.Low.diff().clip(None,0)
    df['Uptrend_Down_Avg'] = df.Uptrend_Down_Pen.rolling(window=window).apply(lambda x: x[x!=0].mean()) # only include non zero numbers in average
    df['Uptrend_Sell_Stop'] = df.Low.rolling(window=2).min() - df.Uptrend_Down_Avg.shift(1) * multiplier
    df['Uptrend_Protected'] = df.Uptrend_Sell_Stop.rolling(window=3).max()

    # for downtrends
    df['Downtrend_Up_Pen'] = df.High.diff().clip(0,None)
    df['Downtrend_Up_Avg'] = df.Downtrend_Up_Pen.rolling(window=window).apply(lambda x: x[x!=0].mean()) # only include non zero numbers in average
    df['Downtrend_Buy_Stop'] = df.High.rolling(window=2).max() + df.Downtrend_Up_Avg.shift(1) * multiplier * 1.5 #wider stops on shorts
    df['Downtrend_Protected'] = df.Downtrend_Buy_Stop.rolling(window=3).min()

    df = df.drop(columns=['Uptrend_Down_Pen',
                     'Uptrend_Down_Avg',
                     'Downtrend_Up_Pen',
                     'Downtrend_Up_Avg',
                     ])

    return df

### return single value functions ###

def average_downside_penetration(main_df, FastEMAPeriod=13):
    df = main_df.copy()  # do not alter original object
    #Calculate downside penetration = down day and points below the EMA
    df['Fast_EMA'] = df.Close.ewm(span=FastEMAPeriod).mean()
    df['Down_Day'] = (df.Close < df.Open)
    df['Penetration'] = df.Close.lt(df.Fast_EMA)
    df['Downside_Pen_Amt'] = (df.Fast_EMA - df.Close) * df.Down_Day * df.Penetration

    # Predict tomorrows EMA
    df['Predicted_EMA'] = df.Fast_EMA + df.Fast_EMA.diff()

    df['Downside_Pen_Amt'] = df['Downside_Pen_Amt'].replace(0, np.nan)
    # get average of last 5 downside penetrations
    ADP = df.Downside_Pen_Amt.dropna().tail(5).mean().round(2)

    # print(f'ADP = {ADP}')

    orderlevel = round(df.Predicted_EMA[-1] - ADP, 2)

    # print(F'Order level = {orderlevel}')
    return orderlevel

def chandelier_exit_long(main_df, period=22):  # default period is 22
    df = main_df.copy()
    df = add_avg_true_range(df)

    df['rolling_high'] = df['High'].rolling(min_periods=period,
                                            window=period,
                                            center=False).max()
    df['chandelier_long'] = df['rolling_high'] - df['Avg TR'] * 3
    cel = df['chandelier_long'][-1].round(2)
    # print(df)
    return cel

def chandelier_exit_short(main_df, period=22):  # default period is 22
    df = main_df.copy()
    df = add_avg_true_range(df)

    df['rolling_low'] = df['Low'].rolling(min_periods=period,
                                          window=period,
                                          center=False).min()
    df['chandelier_short'] = df['rolling_low'] + df['Avg TR'] * 3
    ces = df['chandelier_short'][-1].round(2)
    return ces

def test():
    
    symbol='888.L'
    filepath = config.DATA_DIR + symbol + '.csv'

    # df = md.get_stock_data(symbol)
    df = md.df_from_csv(filepath)
    
    # these return a single value
    adp = average_downside_penetration(df)
    cel = chandelier_exit_long(df)
    ces = chandelier_exit_short(df)

    # these return a dataframe
    df = add_ema(df)
    df = add_force_index(df)
    df = add_macd(df)
    df = add_elder_impulse(df)
    df = add_weekly_elder_impulse(df)
    df = add_elder_bull_divergence(df)
    df = add_avg_true_range(df)
    df = add_auto_envelope(df)
    df = add_safe_zone_stops(df)

    print(df,adp,cel,ces)

if __name__ == "__main__":
    # stuff only to run when not called via 'import' here
    test()