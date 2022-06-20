import pandas as pd

def df_from_csv(file_path):
    # pull some data - when writing and reading back from csv the index is converted to an object type so need to convert back to datetime64 if to be used with finplot
    df = pd.read_csv(file_path)
    df.Date = pd.to_datetime(df.Date, format='%d/%m/%Y')

    # format it in pandas
    df = df.astype({'Date':'datetime64[ns]'})
    df = df.set_index('Date')
    # print(f'Dataframe:\n{df}\ndf datatypes:\n{df.dtypes}')
    return df


# md.download_naked_trades()
df = df_from_csv('./naked trades/Shares.csv')



print(df)
