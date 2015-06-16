




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
