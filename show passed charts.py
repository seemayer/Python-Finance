import os
import plot

for file in os.scandir('screen passed'):
  name = file.name[:-4] 
  print(name)

  try:
    plot.plot_chart(name,'1d')
  except:
    print('uanble to plot '+ name)