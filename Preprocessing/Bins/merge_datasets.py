



#import pandas as pd
#import numpy as np
import os


def put_together_names(filename,fout):
  colnamelist = []
  colnames = {}
  lineind = 0
  for line in open('../../Data/%s.collab' % filename):
    lineind += 1
    colnames[lineind] = line.strip()
    colnamelist.append(line.strip())
  rownamelist = []
  rownames = {}
  lineind = 0
  for line in open('../../Data/%s.rowlab' % filename):
    lineind += 1
    rownames[lineind] = line.strip()
    rownamelist.append(line.strip())
  # write file
  lineind = -1
  for line in open('../../Data/%s.mtx' % filename):
    lineind += 1
    if lineind < 3:
      continue
    words = line.strip().split(' ')
    fout.write('%s %s %s\n' % (rownames[eval(words[0])], colnames[eval(words[1])], words[2]))
  return (rownamelist,colnamelist)
  pass
  
def merge_datasets():
  filenamelist = ['matgoBP','matgoCC','matgoMF','matblastcompressed','matpfam','mattaxo']
  allrownames = []
  allcolnames = []
  fout = open('../../Preprocessing/Results/data.mtx','w')
  for filename in filenamelist:
    (rownames,colnames) = put_together_names(filename,fout)
    allrownames += rownames
    allcolnames += colnames
  fout.close()
  allrownames = list(set(allrownames))
  fout = open('../../Preprocessing/Results/data.rowlab','w')
  fout.write('%s\n' % '\n'.join((allrownames)) )
  fout.close()
  fout = open('../../Preprocessing/Results/data.collab','w')
  fout.write('%s\n' % '\n'.join((allcolnames)) )
  fout.close()
  # renumber
  rowdata = {}
  index = 0
  for name in allrownames:
    index += 1
    rowdata[name] = index
  coldata = {}
  index = 0
  for name in allcolnames:
    index += 1
    coldata[name] = index
  fout = open('../../Preprocessing/Results/tmp','w')
  for line in open('../../Preprocessing/Results/data.mtx'):
    words = line.strip().split(' ')
    fout.write('%d %d %s\n' %( rowdata[words[0]], coldata[words[1]], words[2]))
  fout.close()
  os.system('mv ../../Preprocessing/Results/tmp ../../Preprocessing/Results/data.mtx')
  pass


if __name__ == '__main__':
  merge_datasets()
