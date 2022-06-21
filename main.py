import config
import market_data as md
import technical_indicators as ti
import screens
import output
import pandas as pd

# CORE PROGRAM START

# refresh_core_data
tickers = md.get_list_of_market_tickers('SETS')
# md.reset_market_data(lst_tickers=['CCH.L','PHNX.L','BA.L','ASC.L'])
md.reset_market_data(tickers)


def short_downward_channel():
    # Reset screen passed folder    
    md.del_dir_and_copy_files(src_dir = config.DATA_DIR, tar_dir = config.SCREEN_DIR)
    # Weekly impulse must be red - tide
    screens.weekly_impulse_not_equal('green')
    screens.weekly_impulse_not_equal('blue')
    # Upward wave so that close is above EMA-26
    screens.channel_short() 
    # Keep top 30% weakest performers
    screens.relative_strength(strongest=False) 
    
def long_upward_channel():
    # Reset screen passed folder    
    md.del_dir_and_copy_files(src_dir = config.DATA_DIR, tar_dir = config.SCREEN_DIR)
    # Weekly impulse must be green - tide
    screens.weekly_impulse_not_equal('red')
    screens.weekly_impulse_not_equal('blue')
    # Downward wave based on force index
    screens.force_index(below_zero=True) 
    # Keep top 30% strongest performers
    screens.relative_strength(strongest=True) 

# md.del_dir_and_copy_files(src_dir = config.DATA_DIR, tar_dir = config.SCREEN_DIR)
# screens.elder_triple()
# output.order_levels()
output.channel_order_levels_short()
# CORE PROGRAM END

# md.download_sector_info()
# md.download_SETS_tickers()
# md.get_list_of_market_tickers('SETS')

# df = md.df_from_csv('./data/GSK.L.csv')
# cel = ti.chandelier_exit_long(df)
# print(md.get_list_of_market_tickers('SETS'))

# ti.test()

# md.del_dir_and_copy_files(src_dir = './data/', tar_dir = './screen passed/')

# print(df)

# screens.elder_divergence()
