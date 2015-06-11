

# Protein function prediction

For now, the project aims to reliably predict the function of the transporter protein. The function will be given as the hierarchical structure. Each protein is represented as a set of features, including Gene Ontology, protein familiy, BLAST, and Taxonomy.

## Original data

1. Original data about protein features from different categories are extracted according to the [Master's thesis](), which covers the protein features listed as follows: 

   1. Gene ontology (GO) data

      |Type|#Items|
      |---:|---:|
      |Protein|101422|

      |GO feature type|#Items|
      |---:|---:|
      |Biological process|12891|
      |Molecular function|4816|
      |Cellular component|1670|

   2. Protein family (Pfam) data

      |#Protein|#Taxonomy features|
      |---:|---:|
      |100589|7341|

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
      |matgoBP|10142|12891|
      |matgoCC|101422|1670|
      |matgoMF|101422|4816|
      |matblastcompressed|56838|12646|
      |matpfam|100589|7341|
      |mattaxo|104116|3004|

   1. In the end, we have 

      |#Proteins|#Features|
      |----:|----:|
      |113863|42368|

1. Scripts for data preprocessing are located in `./Preprocessing/` directory.

##
