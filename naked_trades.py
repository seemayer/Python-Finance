from datetime import datetime
import market_data as md
import plot_charts as plot

df = md.df_from_csv('./shares and dates.csv')

# print(df)

for date,share in df.iterrows():
    print(date,share.item())

    date = datetime.strftime(date,'%Y-%m-%d')

    try:
        plot.get_data_and_plot_chart(symbol = share.item(),end=date)
    except:
        print(f'unable to print {share}')


