import pandas as pd

  df = pd.read_csv('data/' + symbol + '.csv', index_col = False)

  print(df) 

  print (df.loc[0])