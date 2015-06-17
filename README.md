

# Protein function prediction

For now, the project aims to reliably predict the function of the transporter proteins. The function is defined as TC code following the hierarchical structure of the transporter protein classification system. In addition to transporter proteins in TCDB, we obtain proteins from UniProt and represent each protein with the following features, including
   1. Gene Ontology
   2. Protein Family
   3. BLAST score with UniProt
   4. Taxonomy in NCBI
   5. BLAST score with TCDB

## Data sources and feature representations 

1. We obtain some feature representations for proteins based on the [Master thesis](). This covers features in the following categories. 

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

  1. Data file for TCDB sequence and classification information is in the file `./Data/tcdb`.


1. [BLAST with TCDB](http://hongyusu.github.io/lessons/2015/06/16/ncbi-blast-installation-and-running-in-parallel/)

   1. Protein sequences are aligned with themselves by running BLAST algorithms.
   1. This procedure will genrate a pairwise similarity matrix.
   1. Instruction for installing and running can be found from [my blog post](http://hongyusu.github.io/lessons/2015/06/16/ncbi-blast-installation-and-running-in-parallel/). 
   1. In particular, after removing some replicated proteins, there are 12515 protein left in TCDB which will be used to build a TCDB BLAST database.
   1. For the BLAST search, we obtain all hits with e-value above 0.01. 
   1. We use BLAST score as similary measure between pair of proteins.
   1. Some statistics about the TCDB BLAST features are shown in the following table

      |Type of Data|Number of items|
      |---:|---:|
      |Protein|12515|
      |TCDB BLAST|12515|

   1. Data file for TCDB BLAST feature is in the file `./Data/tcdbblast`.
      1. The format of this file is `qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore`.

1. [InterProScan](http://hongyusu.github.io/lessons/2015/06/17/extract-protein-features-via-interproscan/)

   1. For all proteins in TCDB, we extract various protein features by running [InterProScan](https://code.google.com/p/interproscan/).
   1. As this procedure takes time, we would like to install and run the InterProScan on local machines other than webservers.
   1. A brief intruction for installation and running InterProScan is documented in [my blog post](http://hongyusu.github.io/lessons/2015/06/17/extract-protein-features-via-interproscan/).
   1. In particular, we download the InterProScan package together with various databases. Version information of InterProScan software and databases can be found from the following table

      |Software and databases|Version|Information|
      |---:|---:|---:|
      |InterProScan|5.13-52.0|InterProScan package|
      |ProDom|2006.1|ProDom is a comprehensive set of protein domain families automatically generated from the UniProt Knowledge Database.|
      |HAMAP||High-quality Automated and Manual Annotation of Microbial Proteomes|
      |SMART|6.2|SMART allows the identification and analysis of domain architectures based on Hidden Markov Models or HMMs|
      |SuperFamily|1.75|SUPERFAMILY is a database of structural and functional annotation for all proteins and genomes.|
      |PRINTS|42.0|A fingerprint is a group of conserved motifs used to characterise a protein family|
      |Panther|9.0|The PANTHER (Protein ANalysis THrough Evolutionary Relationships) Classification System is a unique resource that classifies genes by their functions, using published scientific experimental evidence and evolutionary relationships to predict function even in the absence of direct experimental evidence.|
      |Gene3d|3.5.0|Structural assignment for whole genes and genomes using the CATH domain structure database|
      |PIRSF|3.01|The PIRSF concept is being used as a guiding principle to provide comprehensive and non-overlapping clustering of UniProtKB sequences into a hierarchical order to reflect their evolutionary relationships.|
      |PfamA|27.0|A large collection of protein families, each represented by multiple sequence alignments and hidden Markov models (HMMs)|
      |PrositeProfiles||PROSITE consists of documentation entries describing protein domains, families and functional sites as well as associated patterns and profiles to identify them|
      |TIGRFAM|15.0|TIGRFAMs are protein families based on Hidden Markov Models or HMMs|
      |PrositePatterns||PROSITE consists of documentation entries describing protein domains, families and functional sites as well as associated patterns and profiles to identify them|
      |Coils|2.2|Prediction of Coiled Coil Regions in Proteins|
      |TMHMM| 2.0| Analysis TMHMM-2.0c| 
      |SignalP_GRAM_NEGATIVE |4.0|Analysis SignalP_GRAM_NEGATIVE-4.0 |
      |Phobius |1.01|Analysis Phobius-1.01 |
      |SignalP_EUK |4.0|Analysis SignalP_EUK-4.0 |
      |SignalP_GRAM_POSITIVE |4.0|Analysis SignalP_GRAM_POSITIVE-4.0 |
   
   1. Note that the last five tools are not installed so far. 
   1. It is not necessary to redo the scan with InterProScan for all TCDB sequences as most of the TCDB sequences already have UniProt accession number. Therefore, we depend on the lookup service provided by InterProScan in order to directly extract the sequence features from the database.
   1. In addition to direct extraction, protein sequences that is not known to InterProScan are scanned.

1. Original data files are located in the directory `./Data/`.

## Data preprocessing

1. Remove duplication in transporter protein classification database sequence-classification file.

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

         |Feature name|Prefix|
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
