


import os
import re


def run_rpsblast_rpsdbs():
  '''
  run rps blast on public CDD databases
  '''
  dbs=['Cdd_NCBI','Cdd','Cog','Kog','Pfam','Prk','Smart','Tigr']
  for db in dbs:
    print db
    os.system('''../Blast/ncbi-blast-2.2.31+/bin/rpsblast  -evalue 0.01 -num_threads 4 -outfmt "6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore" -db ../Blast/ncbi-blast-2.2.31+/bin/CDD/%s -query ../../Data/tcdb -out ../../Data/tcdbrps%s ''' % (db,db))


def run_rpsblast_tcdb():
  '''
  run rpsblast on CDD database of all tcdb proteins
  '''
  for line in open('../Blast/ncbi-blast-2.2.31+/bin/db/tcdb201509pssm/tcdb201509pssm.pn'):
    filename = re.sub('.smp','',line.strip())
    print filename
    os.system('''../Blast/ncbi-blast-2.2.31+/bin/rpsblast  -evalue 0.01 -num_threads 4 -outfmt "6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore" -db ../Blast/ncbi-blast-2.2.31+/bin/db/tcdb201509pssm/tcdb201509pssm -query ../Blast/ncbi-blast-2.2.31+/bin/db/tcdb201509pssm/%s -out ../../Data/tcdbrpstcdb201509pssmTMP/%s.resrpstcdb201509pssm ''' % (filename,filename))




if __name__ == '__main__':
  #run_rpsblast_rpsdbs()
  run_rpsblast_tcdb()




