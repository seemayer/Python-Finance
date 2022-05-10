#!/usr/bin/env python3

import os
import pandas as pd

file_names = ['3IN.L.csv','888.L.csv','AAF.L.csv']

for file in os.scandir('./a_test_data/'):
  # print(file.name, file.path)
    if file.name not in file_names:
      os.unlink(file.path)
  