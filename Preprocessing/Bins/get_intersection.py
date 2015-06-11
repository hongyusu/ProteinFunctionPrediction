
import os


def get_intersection():
  t = 0
  proteinlist = []
  for line in open('../../Preprocessing/Results/data_statistics'): 
    words = line.strip().split(' ')
    if eval(words[1]) > t and eval(words[2]) > t and eval(words[3]) > t and eval(words[4]) >t and eval(words[5]) > t:
      proteinlist.append(words[0])
  fout = open('../../Preprocessing/Results/data_intersection','w')
  for line in open('../../Preprocessing/Results/data'):
    words = line.strip().split(' ')
    if words[0] in proteinlist:
      fout.write(line)
  fout.close()
  pass



def compute_statistics():
  s = ''
  ptname = ''
  features = [0,0,0,0,0]
  for line in open('../../Preprocessing/Results/data'):
    words = line.strip().split(' ')
    if ptname == '':
      ptname = words[0]
    if not ptname == words[0]:
      # process
      s += '%s %s\n' % (ptname,' '.join(map(str,features)))
      # initialize
      ptname = words[0]
      features = [0,0,0,0,0]
    if words[1].startswith('G'):
      features[0] += 1
    if words[1].startswith('B'):
      features[1] += 1
    if words[1].startswith('P'):
      features[2] += 1
    if words[1].startswith('T') and not words[1].startswith('TC'):
      features[3] += 1
    if words[1].startswith('TC'):
      features[4] += 1
  s += '%s %s\n' % (ptname,' '.join(map(str,features)))
  fout = open('../../Preprocessing/Results/data_statistics','w')
  fout.write(s)
  fout.close()

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
  Lineind = 0
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
  #compute_statistics()
  #get_intersection()
  rename_files()
