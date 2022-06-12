import numpy as np
import pandas as pd

mydate = np.array(['2001-01-01', '2002-02-03']).astype('datetime64[ns]')

df=pd.DataFrame({'Date':mydate})
print(df.dtypes)
print(df)
