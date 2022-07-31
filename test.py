import pandas as pd

df = pd.read_csv('./data/shares/AAF.L.csv', index_col=False)
df.to_json('./data/aaf.json', orient='records', lines=True)