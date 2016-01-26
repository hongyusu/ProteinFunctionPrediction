

import re

def compute_edgelist(tcdbcollabFilename,EFilename):
  '''
  this script is to generate the edge list of TC hierarchical structure
  '''
  fout = open(EFilename,'w')
  index = 0
  mapper = {}
  res = []
  for line in open(tcdbcollabFilename):
    if line.startswith('TC__'):
      index+=1
      name = re.sub('TC__','',line.strip())
      mapper[name] = index
      names = name.split('.')
      if len(names) < 2:
        continue
      else:
        print '.'.join(names[:len(names)-1]),name
        res.append('%d,%d' % (mapper['.'.join(names[:len(names)-1])],mapper[name]))
  fout.write('\n'.join(res))
  fout.close()


if __name__ == '__main__':
  compute_edgelist('../../Experiments/Data/tcdb.collab','../../Experiments/Data/tcdb.TC.E')
