

# this script need the support of Python pandas package

import pandas as pd
import numpy as np


def merge_datasets():
  filename = '../../Data/matgoBP.mtx' 
  data = np.genfromtxt(filename, delimiter = ' ', skip_header=2, dtype = None, names=True)
  print data.dtype.names

if __name__ == '__main__':
  merge_datasets()