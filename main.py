import market_data as md
import technical_indicators as ti
import screens
import output
import pandas as pd



print(md.get_list_of_market_tickers('SETS'))



# output.order_levels()

# ti.test()



# df = md.get_stock_data('GOOG')
md.reset_market_data(market = 'SETS')

# md.del_dir_and_copy_files(src_dir = './data/', tar_dir = './screen passed/')


# print(df)
# md.reset_market_data(market = 'FTSE350')
# screens.elder_triple()
# screens.relative_strength()
# screens.elder_divergence()

# print(md.get_list_of_market_tickers('FTSE350'))




