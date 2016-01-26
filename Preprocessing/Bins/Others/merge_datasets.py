



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
    tcdbname = 'TC' + words[1]
    fout.write('%s %s 1\n' % (proteinname,tcdbname))
  pass

def process_tcdbblast(filename,fout):
  for line in open('../../Data/tcdbblast'):
    words = line.strip().split('\t')
    proteinname = re.sub('.*\|','',words[0])
    featurename = re.sub('.*\|','',words[1])
    score = re.sub(' .*','',words[11])
    fout.write('%s TB%s %s\n' % (proteinname,featurename,score))
  pass


def put_together_names():
  filenamelist = ['matgoBP','matgoCC','matgoMF','matblastcompressed','matpfam','mattaxo','tcdb','tcdbblast']
  fout = open('../../Preprocessing/Results/data','w')

  # process individual file
  for filename in filenamelist:
    print filename

    if filename == 'tcdb':
      process_tcdb(filename,fout)
      continue
    if filename == 'tcdbblast':
      process_tcdbblast(filename,fout)
      continue


    # rolnames
    colnameprefix = ''
    if filename == 'matgoBP':
      colnameprefix = 'GB'
    if filename == 'matgoCC':
      colnameprefix = 'GC'
    if filename == 'matgoMF':
      colnameprefix = 'GM'
    if filename == 'matblastcompressed':
      colnameprefix = 'M'
    if filename == 'mattaxo':
      colnameprefix = 'M'

    colnames = {}
    lineind = 0
    for line in open('../../Data/%s.collab' % filename):
      lineind += 1
      colnames[lineind] = colnameprefix+line.strip()
    
    # rownames
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

def compute_statistics():
  s = ''
  ptname = ''
  features = [0,0,0,0,0,0,0,0]
  for line in open('../../Preprocessing/Results/data'):
    words = line.strip().split(' ')
    if ptname == '':
      ptname = words[0]
    if not ptname == words[0]:
      # process
      s += '%s %s\n' % (ptname,' '.join(map(str,features)))
      # initialize
      ptname = words[0]
      features = [0,0,0,0,0,0,0,0]
    if words[1].startswith('GM'):
      features[0] += 1
    if words[1].startswith('GB'):
      features[1] += 1
    if words[1].startswith('GC'):
      features[2] += 1
    if words[1].startswith('MB'):
      features[3] += 1
    if words[1].startswith('PF'):
      features[4] += 1
    if words[1].startswith('MT'):
      features[5] += 1
    if words[1].startswith('TB'):
      features[6] += 1
    if words[1].startswith('TC'):
      features[7] += 1
  s += '%s %s\n' % (ptname,' '.join(map(str,features)))
  fout = open('../../Preprocessing/Results/data_statistics','w')
  fout.write(s)
  fout.close()
  pass



if __name__ == '__main__':
  merge_datasets()
  compute_statistics()








