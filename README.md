

# Protein function prediction

## Original data

1. Original data about protein features from different categories are extracted according to the [Master's thesis](), which covers the protein features listed as follows: 

   1. Gene ontology (GO) data

      |Type|#Items|
      |---:|---:|
      |Protein|101421|

      |GO feature type|#Items|
      |---:|---:|
      |Biological process|12891|
      |Molecular function|4816|
      |Cellular component|1670|

   2. Protein family (Pfam) data

      |#Protein|#Taxonomy features|
      |---:|---:|
      |100588|7341|

   3. Blast data

      |#Protein|#Blast features|
      |---:|---:|
      |56837|12646|

   4. Taxonomy data

      |#Protein|#Taxonomy features|
      |---:|---:|
      |104115|3004|

2. Original data files are located in the directory `./Data/`.

## Data preprocessing

1. Merge datasets from different sources:

   1. Merge the following feature types into one matrix

      |Data type|Number of features|
      |----:|----:|
      |matgoBP|12891|
      |matgoCC|1670|
      |matgoMF|4816|
      |matblastcompressed|12646|
      |matpfam|7341|
      |mattaxo|3004|

   1. In the end, we have 

      |#Protein|#Features|
      |----:|----:|
      |113863|42368|

##
