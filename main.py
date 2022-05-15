import config
import market_data as md
import technical_indicators as ti
import screens
import output
import pandas as pd

# CORE PROGRAM START

# tickers = md.get_list_of_market_tickers('FTSE100')
# print(tickers)
md.reset_market_data(lst_tickers=['CCH.L','PHNX.L','BA.L'])
screens.elder_triple()
# screens.relative_strength()
output.order_levels()
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
