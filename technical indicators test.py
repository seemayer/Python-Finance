import market_data as md
import technical_indicators as ti

# df = md.get_stock_data('GOOG')
# df = ti.add_ema(df,37)
# df = ti.add_force_index(df)
# df = ti.add_macd(df)
# df = ti.add_macd_cross(df)
# df = ti.add_elder_impulse(df)
# df = ti.add_elder_bull_divergence(df)
# md.reset_market_data()

md.del_dir_and_copy_files(src_dir = './data/', tar_dir = './screen passed/')


# print(df)