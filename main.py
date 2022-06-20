import config
import market_data as md
import technical_indicators as ti
import screens
import output
import pandas as pd

# CORE PROGRAM START

md.download_naked_trades(earliest_date = '2017-01-01')
df = md.df_from_csv('./naked trades/Shares.csv')

unique = df['Epic'].unique()
print(unique)

for i in unique:
    print(i)
    md.get_stock_data(i+'.L')











# # tickers = md.get_list_of_market_tickers('SETS')
# # print(tickers)
# # md.reset_market_data(lst_tickers=['CCH.L','PHNX.L','BA.L','ASC.L'])
# # md.reset_market_data(lst_tickers=md.get_list_of_market_tickers('SETS'))
# # md.del_dir_and_copy_files(src_dir = config.DATA_DIR, tar_dir = config.SCREEN_DIR)
# # screens.elder_triple()
# # screens.channel_short()
# # screens.weekly_impulse_not_equal('green')
# # screens.weekly_impulse_not_equal('blue')
# # screens.relative_strength(strongest=False)
# # output.order_levels()
# # output.channel_order_levels_short()
# # CORE PROGRAM END

# # md.download_sector_info()
# # md.download_SETS_tickers()
# # md.get_list_of_market_tickers('SETS')

# # df = md.df_from_csv('./data/GSK.L.csv')
# # cel = ti.chandelier_exit_long(df)
# # print(md.get_list_of_market_tickers('SETS'))

# # ti.test()

# # md.del_dir_and_copy_files(src_dir = './data/', tar_dir = './screen passed/')

# # print(df)

# # screens.elder_divergence()
