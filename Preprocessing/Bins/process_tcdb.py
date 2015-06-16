
import re



def process_tcdb_for_blast():
  data = []
  write = 0
  fout = open('/cs/fs/home/su/softwares/blast/bin/tcdb','w')
  for line in open('../../Data/tcdb'):
    if line.startswith('>'):
      words = line.strip().split('|')
      proteinname = (words[2]).upper()
      if not proteinname in data:
        write = 1
        data.append(proteinname)
        fout.write("%s|TCDB|%s %s\n" % (words[0],proteinname,words[3]))
      else:
        write = 0
        print proteinname
    else:
      if write == 1:
        fout.write(line)
  fout.close()
  pass



def process_tcdb_label():
  rownamelist = []
  colnamelist = []
  fout_row = open('../../Data/tcdb.rowlab','w')
  fout_col = open('../../Data/tcdb.collab','w')
  for line in open('../../Data/tcdb'):
    if line.startswith('>'):
      words = line.strip().split('|')
      if not words[2].upper() in rownamelist:
        rownamelist.append(words[2])
      colname = re.sub(' .*','',words[3])
      if not colname.upper() in colnamelist:
        colnamelist.append(colname)
  fout_row.write('%s' % ('\n'.join(rownamelist)))
  fout_col.write('%s' % ('\n'.join(colnamelist)))
  fout_col.close()
  fout_row.close()
  pass



if __name__ == '__main__':
  process_tcdb_for_blast()
  process_tcdb_label()
