



#import pandas as pd
#import numpy as np
import os
import re


def process_tcdb(filename,fout):
  for line in open('../../Data/tcdb'):
    if not line.startswith('>'):
      continue
    words = line.strip().split('|')
    proteinname = re.sub(' ','',words[2])
    tcdbname = 'TC' + re.sub(' .*','',words[3]) 
    fout.write('%s %s %d\n' % (proteinname,tcdbname,1))
  pass

def put_together_names():
  filenamelist = ['matgoBP','matgoCC','matgoMF','matblastcompressed','matpfam','mattaxo','tcdb']
  fout = open('../../Preprocessing/Results/data','w')

  for filename in filenamelist:
    if filename == 'tcdb':
      process_tcdb(filename,fout)
      continue

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
    lineind = -1
    for line in open('../../Data/%s.mtx' % filename):
      lineind += 1
      if lineind < 3:
        continue
      words = line.strip().split(' ')
      fout.write('%s %s %s\n' % (rownames[eval(words[0])], colnames[eval(words[1])], words[2]))

  fout.close()
  pass

def rename_files():
  # get row and col labels
  os.system(""" cat ../../Preprocessing/Results/data | awk -F' ' '{print $1}' | sort|uniq > ../../Preprocessing/Results/data.rowlab """)
  os.system(""" cat ../../Preprocessing/Results/data | awk -F' ' '{print $2}' | sort|uniq > ../../Preprocessing/Results/data.collab """)
  os.system(""" cat ../../Preprocessing/Results/data |  sort -k1,1 -k2,2  > ../../Preprocessing/Results/tmp; mv ../../Preprocessing/Results/tmp ../../Preprocessing/Results/data """)
  # rename
  colnames = {}
  rownames = {}
  lineind = 0
  for line in open('../../Preprocessing/Results/data.collab'):
    lineind += 1
    colnames[line.strip()] = lineind
  rownames = {}
  Lineind = 0
  for line in open('../../Preprocessing/Results/data.rowlab'):
    lineind += 1
    rownames[line.strip()] = lineind
  fout = open('../../Preprocessing/Results/data.mtx', 'w')
  for line in open('../../Preprocessing/Results/data'):
    words = line.strip().split(' ')
    fout.write('%d %d %s\n' % ( rownames[words[0]], colnames[words[1]], words[2]  ))
  fout.close()
  pass



def merge_datasets():
  put_together_names()
  rename_files()
  pass


if __name__ == '__main__':
  merge_datasets()








