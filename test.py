import finplot as fplt
import yfinance as yf
import market_data as md
import os
import config
from pathlib import Path

from datetime import datetime
from dateutil.relativedelta import relativedelta

end = datetime.strftime(datetime.today(),'%Y-%m-%d')
print(end)
exit()

end = datetime.strptime(end,'%Y-%m-%d')
start = end - relativedelta(years=1)

end = datetime.strftime(end,'%Y-%m-%d')
start = datetime.strftime(start,'%Y-%m-%d')

print(start,end)

df = yf.download('GOOG',
                interval='1d',
                end=end,
                start=start)


  


