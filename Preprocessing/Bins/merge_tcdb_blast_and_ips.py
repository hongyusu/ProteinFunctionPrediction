





#import pandas as pd
#import numpy as np
import os
import re


def process_tcdb(filename,fout):
  for line in open('../../Data/tcdb'):
    if not line.startswith('>'):
      continue
    words = line.strip().split('|')
    words = words[2].split(' ')
    proteinname = words[0]
    #tcdbname = '.'.join(words[1].split('.')[0:4])
    fout.write('%s TC__%s 1\n' % (proteinname,'.'.join(words[1].split('.')[0:1])))
    fout.write('%s TC__%s 1\n' % (proteinname,'.'.join(words[1].split('.')[0:2])))
    fout.write('%s TC__%s 1\n' % (proteinname,'.'.join(words[1].split('.')[0:3])))
    fout.write('%s TC__%s 1\n' % (proteinname,'.'.join(words[1].split('.')[0:4])))
  pass

def process_tcdbblast(filename,fout):
  for line in open('../../Data/tcdbblast'):
    words = line.strip().split('\t')
    proteinname = re.sub('.*\|','',words[0])
    featurename = re.sub('.*\|','',words[1])
    score = re.sub(' *','',words[11])
    fout.write('%s TB__%s %s\n' % (proteinname,featurename,score))
  pass

def process_tcdbips(filename,fout):
  '''
  process tcdb interproscan results
  '''
  for line in open('../../Data/tcdbips'):
    words = line.strip().split('\t')
    proteinname = re.sub('.*\|','',words[0])
    featurename = words[3] +'__'+ words[4]
    if words[8] == '-':
      words[8] = '1'
    fout.write('%s TI%s %s\n' % (proteinname,featurename,words[8]))
  pass


def put_together_names():
  filenamelist = ['tcdb','tcdbblast','tcdbips']
  fout = open('../../Preprocessing/Results/tcdbdata','w')

  # process individual file
  for filename in filenamelist:
    print filename

    if filename == 'tcdb':
      process_tcdb(filename,fout)
      continue
    if filename == 'tcdbblast':
      process_tcdbblast(filename,fout)
      continue
    if filename == 'tcdbips':
      process_tcdbips(filename,fout)
      continue

  fout.close()
  pass

def rename_files():
  # get row and col labels
  os.system(""" cat ../../Preprocessing/Results/tcdbdata | awk -F' ' '{print $1}' | sort|uniq > ../../Preprocessing/Results/tcdbdata.rowlab """)
  os.system(""" cat ../../Preprocessing/Results/tcdbdata | awk -F' ' '{print $2}' | sort|uniq > ../../Preprocessing/Results/tcdbdata.collab """)
  os.system(""" cat ../../Preprocessing/Results/tcdbdata |  sort -k1,1 -k2,2  > ../../Preprocessing/Results/tmp; mv ../../Preprocessing/Results/tmp ../../Preprocessing/Results/tcdbdata """)
  # rename
  colnames = {}
  rownames = {}
  lineind = 0
  for line in open('../../Preprocessing/Results/tcdbdata.collab'):
    lineind += 1
    colnames[line.strip()] = lineind
  rownames = {}
  lineind = 0
  for line in open('../../Preprocessing/Results/tcdbdata.rowlab'):
    lineind += 1
    rownames[line.strip()] = lineind
  fout = open('../../Preprocessing/Results/tcdbdata.mtx', 'w')
  for line in open('../../Preprocessing/Results/tcdbdata'):
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



