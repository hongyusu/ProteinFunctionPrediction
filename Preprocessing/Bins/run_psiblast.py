


import os
import re



def psiblast():
  fout_namelist = open('../Blast/ncbi-blast-2.2.31+/bin/db/tcdb201509pssm/tcdb201509pssm.pn','w')
  for line in open('../../Data/tcdb'):
    if line.startswith('>'):
      try:
        fout.close()
        os.system('''../Blast/ncbi-blast-2.2.31+/bin/psiblast -num_iterations 10 -evalue 0.01 -num_threads 4 -outfmt "6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore" -db ../Blast/ncbi-blast-2.2.31+/bin/db/tcdb201509 -query %s -out %s.res -out_pssm %s.smp ''' % (filename,filename,filename))
      except:
        pass 
      filename = re.sub('.*\|','',re.sub(' .*','',line.strip()))
      fout_namelist.write('%s.smp\n' % filename)
      filename = '../Blast/ncbi-blast-2.2.31+/bin/db/tcdb201509pssm/'+filename
      fout = open(filename,'w')
      fout.write(line)
    else:
      fout.write(line)
  pass
  fout.close()
  os.system('''../Blast/ncbi-blast-2.2.31+/bin/psiblast -num_iterations 10 -evalue 0.01 -num_threads 4 -outfmt "6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore" -db ../Blast/ncbi-blast-2.2.31+/bin/db/tcdb201509 -query %s -out %s.res -out_pssm %s.smp ''' % (filename,filename,filename))
  fout_namelist.close()

if __name__ == '__main__':
  psiblast()


