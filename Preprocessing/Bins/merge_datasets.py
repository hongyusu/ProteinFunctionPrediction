



#import pandas as pd
#import numpy as np



def put_together_names(filename):
  colnames = {}
  lineind = 0
  for line in open('../../Data/%s.collab' % filename):
    lineind += 1
    colnames[lineind] = line.strip()
  rownames = {}
  lineind = 0
  for line in open('../../Data/%s.rowlab' % filename):
    lineind += 1
    rownames[lineind] = line.strip()
  # write file
  fout = open('../../Preprocessing/Results/%s.adj' % filename,'w')
  lineind = -1
  for line in open('../../Data/%s.mtx' % filename):
    lineind += 1
    if lineind < 3:
      continue
    words = line.strip().split(' ')
    fout.write('%s %s %s\n' % (rownames[eval(words[0])], colnames[eval(words[1])], words[2]))
  fout.close()
  pass
  
def merge_datasets():
  filename = '../../Data/matgoBP.mtx' 
  data = np.genfromtxt(filename, delimiter = ' ', skip_header=2, dtype = None, names=True)
  print data.dtype.names
  pass


if __name__ == '__main__':
  filenamelist = ['matgoBP','matgoCC','matgoMF','matblastcompressed','matpfam','mattaxo']
  for filename in filenamelist:
    put_together_names(filename)
  #merge_datasets()
