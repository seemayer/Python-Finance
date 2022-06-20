import market_data as md
import plot_object as plot

# md.download_naked_trades()

df = md.df_from_csv('./data/888.L.csv')

plt = plot.myplot()

plt.create()
plt.add_candles(df)
plt.add_hline(df,260,start_date='2022-05-03', length=10)
plt.add_hline(df,320)
plt.add_marker(df,'2022-05-03',260,color='#f00')
plt.add_marker(df,'2022-05-03',240,color='#0f0')
plt.add_marker(df,'2022-05-03',220,color='#00f')
plt.add_exponential_moving_average(df,30)
# plt.plot_specific_dates('2021-12-21','2022-01-25')
plt.add_macd(df)
plt.show()