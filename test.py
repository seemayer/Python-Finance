import pandas as pd

def letgo(df = df):
    df.drop('b', axis=1, inplace=True)

frm = pd.DataFrame({'a':[1,2], 'b':[3,4]})
print(frm)
letgo(frm)  # will alter frm
print(frm)


