


# Directory for Blast tools



1. Build TCDB Blast database with TCDB protein sequences via the following command
   `./makeblastdb -in db/tcdb201509 -parse_seqids -dbtype prot`


1. Download CDD source files from NCBI FTP server ftp://ftp.ncbi.nih.gov/pub/mmdb/cdd//cdd.tar.gz.
1. Download CDD version file from NCBI FTP server ftp://ftp.ncbi.nih.gov/pub/mmdb/cdd//cdd.info.
1. Download PSSM version file from NCBI FTP server ftp://ftp.ncbi.nih.gov/pub/mmdb/cdd//cdd.versions.
1. Build CDD databases from different sources by NCBI Blast+ tool with the following command.
   `../makeprofiledb -title SMART     -in Smart.pn -out Smart -threshold 9.82 -scale 100.0 -dbtype rps -index true`

   `../makeprofiledb -title Pfam      -in Pfam.pn -out Pfam -threshold 9.82 -scale 100.0 -dbtype rps -index true`

   `../makeprofiledb -title COG       -in Cog.pn -out Cog -threshold 9.82 -scale 100.0 -dbtype rps -index true`

   `../makeprofiledb -title KOG       -in Kog.pn -out Kog -threshold 9.82 -scale 100.0 -dbtype rps -index true`

   `../makeprofiledb -title CDD_NCBI  -in Cdd_NCBI.pn -out Cdd_NCBI -threshold 9.82 -scale 100.0 -dbtype rps -index true`

   `../makeprofiledb -title PRK       -in Prk.pn -out Prk -threshold 9.82 -scale 100.0 -dbtype rps -index true`

   `../makeprofiledb -title Tigr      -in Tigr.pn -out Tigr -threshold 9.82 -scale 100.0 -dbtype rps -index true`

1. A CDD database covering all sources can be built with the following command 
   `../makeprofiledb -title CDD       -in Cdd.pn -out Cdd -threshold 9.82 -scale 100.0 -dbtype rps -index true`




