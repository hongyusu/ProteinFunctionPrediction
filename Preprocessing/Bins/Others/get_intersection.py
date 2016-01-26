
import os
import numpy as np

def get_intersection():
  t = 0
  proteinlist = []
  for line in open('../../Preprocessing/Results/data_statistics'): 
    words = line.strip().split(' ')
    myarray = np.array(map(float, words[1:len(words)]))>0
    if sum(myarray[0:3] >t)>=1 and sum(myarray[3:9]>t)>=5: 
      proteinlist.append(words[0])
  print proteinlist
  fout = open('../../Preprocessing/Results/data_intersection','w')
  for line in open('../../Preprocessing/Results/data'):
    words = line.strip().split(' ')
    if words[0] in proteinlist:
      fout.write(line)
  fout.close()
  pass



def rename_files():
  os.system('cp ../../Preprocessing/Results/data.collab ../../Preprocessing/Results/data_intersection.collab')
  os.system(""" cat ../../Preprocessing/Results/data_intersection | sed 's/ .*//g' | sort|uniq > ../../Preprocessing/Results/data_intersection.rowlab  """)
  # rename
  colnames = {}
  rownames = {}
  lineind = 0
  for line in open('../../Preprocessing/Results/data_intersection.collab'):
    lineind += 1
    colnames[line.strip()] = lineind
  rownames = {}
  lineind = 0
  for line in open('../../Preprocessing/Results/data_intersection.rowlab'):
    lineind += 1
    rownames[line.strip()] = lineind
  fout = open('../../Preprocessing/Results/data_intersection.mtx', 'w')
  for line in open('../../Preprocessing/Results/data_intersection'):
    words = line.strip().split(' ')
    fout.write('%d %d %s\n' % ( rownames[words[0]], colnames[words[1]], words[2]  ))
  fout.close()
  pass


if __name__ == '__main__':
  get_intersection()
  rename_files()
