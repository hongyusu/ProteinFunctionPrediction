
import re
import os


def process_tcdb_for_blast():
  '''
  process tcdb database for blast serach: remove dupliate proteins etc.
  '''
  data = []
  write = 0
  fout = open('/cs/fs/home/su/softwares/blast/bin/tcdb','w')
  for line in open('../../Data/tcdb.1'):
    if line.startswith('>'):
      words = line.strip().split('|')
      proteinname = (words[2]).upper()
      if not proteinname in data:
        write = 1
        data.append(proteinname)
        fout.write("%s|TC-DB|%s %s\n" % (words[0],proteinname,words[3]))
      else:
        write = 0
        print proteinname
    else:
      if write == 1:
        fout.write(line)
  fout.close()
  os.system('cp /cs/fs/home/su/softwares/blast/bin/tcdb ../../Data/tcdb')
  pass



def process_tcdb_label():
  rownamelist = []
  colnamelist = []
  fout_row = open('../../Data/tcdb.rowlab','w')
  fout_col = open('../../Data/tcdb.collab','w')
  for line in open('../../Data/tcdb'):
    if line.startswith('>'):
      words = line.strip().split('|')
      words = words[2].split(' ')
      proteinname = words[0].upper()
      tcname = words[1].upper()
      if not proteinname in rownamelist:
        rownamelist.append(proteinname)
      if not tcname in colnamelist:
        colnamelist.append(tcname)
  fout_row.write('%s' % ('\n'.join(rownamelist)))
  fout_col.write('%s' % ('\n'.join(colnamelist)))
  fout_col.close()
  fout_row.close()
  pass



if __name__ == '__main__':
  process_tcdb_for_blast()
  process_tcdb_label()
