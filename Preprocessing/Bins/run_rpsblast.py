


import os


def run_rpsblast_rpsdbs():
  dbs=['Cdd_NCBI','Cdd','Cog','Kog','Pfam','Prk','Smart','Tigr']
  for db in dbs:
    print db
    os.system('''../Blast/ncbi-blast-2.2.31+/bin/rpsblast  -evalue 0.01 -num_threads 4 -outfmt "6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore" -db ../Blast/ncbi-blast-2.2.31+/bin/CDD/%s -query ../../Data/tcdb -out ../../Data/tcdbrps%s ''' % (db,db))


def run_rpsblast_tcdb():
  dbs=['tcdb201509pssm']
  for db in dbs:
    print db
    os.system('''../Blast/ncbi-blast-2.2.31+/bin/rpsblast  -evalue 0.01 -num_threads 4 -outfmt "6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore" -db ../Blast/ncbi-blast-2.2.31+/bin/CDD/%s -query ../../Data/tcdb -out ../../Data/tcdbrps%s ''' % (db,db))



if __name__ == '__main__':
  #run_rpsblast_rpsdbs()
  run_rpsblast_tcdb()




