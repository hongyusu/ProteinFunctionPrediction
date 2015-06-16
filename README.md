

# Protein function prediction

For now, the project aims to reliably predict the function of the transporter proteins. The function is defined as TC code following the hierarchical structure of the transporter protein classification system. In addition to transporter proteins in TCDB, we obtain proteins from UniProt and represent each protein with the following features, including
   1. Gene Ontology
   2. Protein Family
   3. BLAST score with UniProt
   4. Taxonomy in NCBI
   5. BLAST score with TCDB

## Data sources and feature representations 

1. We obtain some feature representations for proteins based on the [Master's thesis](). This covers features in the following categories. 

   1. Features from Gene ontology (GO)

      |Type of data|Number of items|
      |---:|---:|
      |Protein|101422|
      |GO: Biological process|12891|
      |GO: Molecular function|4816|
      |GO: Cellular component|1670|

   2. Protein family (Pfam) data

      |Type of data|Number of items|
      |---:|---:|
      |Protein|100589|
      |Pfam feature| 7341|

   3. Blast score with UniProt

      |Type of data|Number of items|
      |---:|---:|
      |Protein|56838|
      |Blast feature|12646|

   4. Taxonomy data

      |Type of data|Number of items|
      |---:|---:|
      |Protein|104116|
      |Taxonomy feature|3004|

1. Transport protein classification data are downloaded from [TCDB database](http://www.tcdb.org/public/). 

   |Type of data|Number of items|
   |---:|---:|
   |Protein|12515|
   |TCDB annotation|9456|

   1. The annotation of TCDB follows a five level classificaiton hierarchy. The number of annoations in each level is shown in the following table

      |Level|Number of annotations|
      |---:|---:|
      |1|7| 
      |2|30| 
      |3|867| 
      |4|2237| 
      |5|9456| 


1. BLAST with TCDB

   1. TCDB proteins are compared with themselves by running BLAST algorithms in order to obtain a pairwise similarity matrix.
   1. Instruction for BLAST installation and running can be found from [my blog post](http://hongyusu.github.io/lessons/2015/06/16/ncbi-blast-installation-and-running-in-parallel/). 
   1. After removing replicated proteins, there are 12515 protein left in TCDB.
   1. For the BLAST search, we obtain all hits with e-value above 0.01. 

      |Type of data|Number of items|
      |---:|---:|
      |Protein|12515|
      |TCDB BLAST|12515|

1. Original data files are located in the directory `./Data/`.

## Data preprocessing

1. Merge datasets from different sources:

   1. Merge the following feature types into one matrix

      |Data type|#Proteins|#Features|
      |----:|----:|----:|
      |matgoBP|101422|12891|
      |matgoCC|101422|1670|
      |matgoMF|101422|4816|
      |matblastcompressed|56838|12646|
      |matpfam|100589|7341|
      |mattaxo|104116|3004|
      |TCDB|12516|9456|

   2. A big global matrix is computed by concatenating the matrices of protein-GO, protein-Blast, protein-Ffam, protein-taxonomy, and protein-TCDB, and protein-TCDBblast.

      1. The number of proteins and the number of features in the union of the collection of matrices are shown in the following table.

      2. The number of proteins and the number of features in the intersection of the collection of matrics are shown in the following table. Notice that a protein will present in the interection matrix if it has features in GO/BLAST/Pfam/Taxonomy categories. 

         |Type|#Proteins|#Features|
         |----:|----:|----:|
         |Union|123619|64328|
         |Intersection|1336|64328|

      3. Different type of fetures are annotated in `.collab` according to the following table

         |Prefix|Feature type|
         |---:|---:|
         |Gene ontology: biological process|GB|
         |Gene ontology: cellular component|GC|
         |Gene ontology: molecular function|GM|
         |Protein family|PF|
         |BLAST|MB|
         |Taxonomy|MT|
         |TCDB classification|TC|
         |TCDB BLAST|TB|

1. Scripts for data preprocessing are located in `./Preprocessing/Bin/`. 
1. Results for data preprocessing are located in `./Preprocessing/Results/`. 

##
