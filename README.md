

# Protein function prediction

For now, the project aims to reliably predict the function of the transporter proteins. The function is defined as TC code following the hierarchical structure of the transporter protein classification system. In addition to transporter proteins in TCDB, we obtain proteins from UniProt and represent each protein with the following features, including
   1. Gene Ontology
   2. Protein Family
   3. BLAST score with UniProt
   4. Taxonomy in NCBI
   5. BLAST score with TCDB

## Feature representation of proteins 

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

   3. Blast data

      |#Protein|#Blast features|
      |---:|---:|
      |56838|12646|

   4. Taxonomy data

      |#Protein|#Taxonomy features|
      |---:|---:|
      |104116|3004|

1. TCDB data are download from [TCDB database](http://www.tcdb.org/public/). 

   |#Protein|#TCDB annotations|
   |---:|---:|
   |12516|9456|

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

   2. A big global matrix is computed by concatenating the matrices of protein-GO, protein-Blast, protein-Ffam, protein-taxonomy, and protein-TCDB.

      1. The number of proteins and the number of features in the union of the collection of matrices are shown in the following table.

      2. The number of proteins and the number of features in the intersection of the collection of matrics are shown in the following table. Notice that a protein will present in the interection matrix if it has features in GO/BLAST/Pfam/Taxonomy categories. 

      |Type|#Proteins|#Features|
      |----:|----:|----:|
      |Union|123610|51824|
      |Intersection|1336|51824|

1. Scripts for data preprocessing are located in `./Preprocessing/`. 

##
