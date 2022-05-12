import pandas as pd
import technical_indicators as ti
import market_data as md
import os 

# delete all files in screen passed folder
lst_screen_passed = []

# md.del_dir_and_copy_files(src_dir = './data/', tar_dir = './screen passed/')

#Screen 1 - Weekly impulse
for file in os.scandir('./screen passed/'):

  df = md.df_from_csv(file.path)

  #calculate indicators for each ticker and add to dataframe
  try:
    df = ti.add_elder_bull_divergence(df, period=40)

    #check last 5 days to see if screen was passed
    screenpassed = any(df.divergence.tail(5))
    print(file.name)
  
    # save data as csv
    if screenpassed:
      lst_screen_passed.append(file.name)
  except:
    print(f'Unable to calc for {file.name}')
  
# saving export list
df = pd.DataFrame(data={"stock": lst_screen_passed})
df.to_csv("./SCREEN_PASSED.csv", sep=',',index=False)

print(lst_screen_passed)

for file in os.scandir('./screen passed/'):
  # print(file.name, file.path)
    if file.name not in lst_screen_passed:
      os.unlink(file.path)