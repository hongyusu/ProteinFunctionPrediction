

# Protein function prediction


## Introduction

For now, the project aims to reliably predict the function of the transporter proteins.
The function is defined as TC code following the hierarchical structure of the transporter protein classification system.
The hierarchical structure of the classification system has five level. We aim to predict the first four level as the fifth level is the very specific classification.
In addition to the transporter proteins documented in TCDB, we also collect proteins from UniProt.
Uniprot proteins have the following features:

   1. Gene Ontology
   2. Protein Family
   3. BLAST score with UniProt
   4. Taxonomy in NCBI

For TCDB proteins we extract features of the following two categorises

   1. BLAST score with TCDB
   2. Several InterProScan feature

## Data

### Data from [Master thesis]() work
 
We obtain some feature representations for proteins based on the [Master thesis](). This covers features in the following categories. 

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

### Other data

We extract protein classification data from TCDB database.
As the intersection of the protein data listed above and the ones in TCDB is very small we compute protein features via BLAST and InterProScan.

1. Transport protein classification data are downloaded from [TCDB database](http://www.tcdb.org/public/). 
NOTE: Su, her you should specify which version has been considered (I guess a version after 7 june)

   |Type of data|Number of items|
   |---:|---:|
   |Protein|12515|
   |TCDB annotation|9456|

   1. The annotation of TCDB follows a five level classification hierarchy. The number of classes in each level is shown in the following table

      |Level|Number of classes|
      |---:|---:|
      |1|7| 
      |2|30| 
      |3|867| 
      |4|2237| 
      |5|9456| 

  1. Data file for TCDB sequence and classification information is in the file `./Data/tcdb.1`.


1. [BLAST with TCDB](http://hongyusu.github.io/lessons/2015/06/16/ncbi-blast-installation-and-running-in-parallel/)

   1. Protein sequences are aligned with themselves by running BLAST algorithms.
   1. This procedure will genrate a pairwise similarity matrix.
   1. Instruction for installing and running BLAST can be found from [my blog post](http://hongyusu.github.io/lessons/2015/06/16/ncbi-blast-installation-and-running-in-parallel/). 
   1. In particular, after removing some replicated proteins, there are 12515 protein left in TCDB which will be used to build a TCDB BLAST database.
   1. The cleaned TCDB data file is located in `./Data/tcdb`.
   1. For the BLAST search, we obtain all hits with e-value below 0.01. 
   1. We use BLAST score as similary measure between pair of proteins.
   1. Some statistics about the TCDB BLAST features are shown in the following table

      |Type of Data|Number of items|
      |---:|---:|
      |Protein|12515|
      |TCDB BLAST feature|12515|

   1. Data file for TCDB BLAST feature is located as `./Data/tcdbblast`.

      1. The format of this file is

         `qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore`.
       
      2. The keywords are explained in the following table

         |Keyword|Representation|
         |---:|---:|
         |qseqid | Query Seq-id|
         |sseqid | Subject Seq-id|
         |sallacc | All subject accessions|
         |qstart | Start of alignment in query|
         |qend | End of alignment in query|
         |sstart | Start of alignment in subject|
         |send | End of alignment in subject|
         |evalue | Expect value|
         |bitscore | Bit score|
         |score | Raw score|
         |length | Alignment length|
         |pident | Percentage of identical matches|
         |mismatch | Number of mismatches|
         |gapopen | Number of gap openings|


1. [InterProScan](http://hongyusu.github.io/lessons/2015/06/17/extract-protein-features-via-interproscan/)

   1. For all proteins in TCDB, we extract various protein features by running [InterProScan](https://code.google.com/p/interproscan/).
   1. As this procedure takes time, we would like to install and run the InterProScan on local machines other than on webservers.
   1. A brief instruction for installation and running InterProScan is documented in [my blog post](http://hongyusu.github.io/lessons/2015/06/17/extract-protein-features-via-interproscan/).
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
      |TMHMM| 2.0| Prediction of transmembrane helices in proteins| 
      |Phobius |1.01|A combined transmembrane topology and signal peptide predictor|
      |SignalP_GRAM_NEGATIVE |4.0|SignalP (organism type gram-negative prokaryotes) predicts the presence and location of signal peptide cleavage sites in amino acid sequences for gram-negative prokaryotes|
      |SignalP_EUK |4.0|SignalP (organism type eukaryotes) predicts the presence and location of signal peptide cleavage sites in amino acid sequences for eukaryotes.|
      |SignalP_GRAM_POSITIVE |4.0|SignalP (organism type gram-positive prokaryotes) predicts the presence and location of signal peptide cleavage sites in amino acid sequences for gram-positive prokaryotes|
   
   1. Note that the last five tools and Panthon database are installed into InterProScan manually.
   1. It is not necessary to perform again the scanning with InterProScan for all TCDB sequences as most of the TCDB sequences already have UniProt accession number. Therefore, we depend on the lookup service provided by InterProScan in order to directly extract the sequence features from the database.
   1. In addition to direct extraction, protein sequences that is not known to InterProScan are scanned.
   1. Interproscan results is located as `./Data/tcdbips`. The file follows the structure described in the following table

      |Column|Description|
      |---:|---:|
      |1|Protein Accession (e.g. P51587)|
      |2|Sequence MD5 digest (e.g. 14086411a2cdf1c4cba63020e1622579)|
      |3|Sequence Length (e.g. 3418)|
      |4|Analysis (e.g. Pfam / PRINTS / Gene3D)|
      |5|Signature Accession (e.g. PF09103 / G3DSA:2.40.50.140)|
      |6|Signature Description (e.g. BRCA2 repeat profile)|
      |7|Start location|
      |8|Stop location|
      |9|Score - is the e-value of the match reported by member database method (e.g. 3.1E-52)|
      |10|Status - is the status of the match (T: true)|
      |11|Date - is the date of the run|
      |12|InterPro annotations - accession (e.g. IPR002093)|
      |13|InterPro annotations - description (e.g. BRCA2 repeat) |
      |14|GO annotations (e.g. GO:0005515) |
      |15|Pathways annotations (e.g. REACT_71) |

1. Besides the data files described above, all original data are located in the directory `./Data/`


## Data preprocessing

1. The first strategy we used is to merge the protein data from the Master thesis and from TCDB database to find an intersection of proteins with both various features and classification information in TCDB.
   1. However, we found out that the intersection is very small. Only about 1000 proteins from TCDB has feature representations in the Master thesis data.
   1. Anywauy, this strategy is briefly illustrated as followings:
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
   
1. Realizing that I cannot rely on the data used in the Master thesis, I directly work on proteins from TCDB. In particular, I compuate various protein features via running BLAST search and InterProScan.
  
   1. First I remove duplicated proteins from the transporter protein classification database (TCDB), particularly, by analyzing the sequence-classification data file.
   
NOTE: In this way you removed the annotations for proteins having multiple annotation paths. These are 29:
AC	      TC
D4ZJA6	1.A.30.1.5
D4ZJA6	1.A.30.1.6
O24303	1.A.18.1.1
O24303	3.A.9.1.1
O34840	2.A.19.2.7
O34840	2.A.19.2.11
P0AAW9	8.A.50.1.1
P0AAW9	2.A.6.2.2
P0C1S5	9.A.39.1.3
P0C1S5	9.A.39.1.2
P18409	1.B.33.3.1
P18409	1.B.8.6.1
P23644	3.A.8.1.1
P23644	1.B.8.2.1
P25568	2.A.1.24.1
P25568	9.A.15.1.1
P28795	9.A.17.1.1
P28795	3.A.20.1.5
P29340	3.A.20.1.1
P29340	3.A.20.1.5
P34230	3.A.1.203.2
P34230	3.A.1.203.6
P94360	3.A.1.1.26
P94360	3.A.1.1.34
Q03PY5	3.A.1.28.2
Q03PY5	3.A.1.26.9
Q03PY7	3.A.1.28.2
Q03PY7	3.A.1.26.9
Q07418	9.A.17.1.1
Q07418	3.A.20.1.5
Q15049	9.B.129.1.1
Q15049	2.A.1.76.1
Q55JG4	9.B.178.1.5
Q55JG4	9.B.178.1.6
Q6GHV7	9.A.39.1.1
Q6GHV7	9.A.39.1.2
Q6GUB0	2.A.88.1.1
Q6GUB0	3.A.1.25.1
Q72L52	3.A.1.1.24
Q72L52	3.A.1.1.25
Q8EAG6	1.A.30.1.5
Q8EAG6	1.A.30.1.6
Q8KQR1	9.A.39.1.4
Q8KQR1	9.A.39.1.2
Q99257	1.I.1.1.1
Q99257	3.A.22.1.1
Q9FBS5	3.A.1.1.42
Q9FBS5	3.A.1.1.43
Q9FBS6	3.A.1.1.42
Q9FBS6	3.A.1.1.43
Q9FBS7	3.A.1.1.42
Q9FBS7	3.A.1.1.43
Q9L0Q1	3.A.1.1.33
Q9L0Q1	3.A.1.1.36
Q9RL01	2.A.1.72.1
Q9RL01	2.A.1.15.15
Q9Y3Q4	1.A.1.5.10
Q9Y3Q4	1.A.1.5.11

If we consider only the annotation till to the fourth level we have only 13 proteins with multiple annotated paths, but in this way we miss (considering annotations from the first to the fourth level) 41 annotations. To my opinion it is not a good idea to eliminate such annotations. Considering that in practice there are only a few multiple paths, we can ignore multiple paths in our predictions, but without removing them from the data. You can recover the full TCDB annotations using the file tcdb.1 instead of tcdb in the Data directory.

   1. Then I run BLAST search and InterProScan for all preprocessed proteins.
   1. Merge TCDB classification (protein labels), TCDB BLAST features, and TCDB InterProScan features.
   1. Make data matrices of different types, e.g., different feature matrices and label matrix.
   1. Important scripts and result files are listed as follows.

      ```
      Preprocessing
      |--Bins
          |---process_tcdb.py        # process original TCDB database (remove duplication ect)
          |---merge_tcdb_blast_and_ips.py          # merge TCDB blast, ips and classfiication data
          |---run_blast.sh           # run BLAST search
          |---run_interproscan.sh    # run interproscan search to generate protein features
          |---separate_different_features.py # generate feature matrices of different types
      |---Results
          |---tcdbdata               # merged data in sparse matrix format: 'protein name' 'feature name' 'value' 
          |---tcdbdata.collab        # feature names
          |---tcdbdata.rowlab        # protein names
          |---tcdbdata.mtx           # sparse data matrix with format 'protein id' 'feature id' 'value'
      Experiments
      |---Data
          |---tcdb.prefix       # data matrices of different type, where type information are explained in the section of Data statistics.
      ```
 
## Data statistics

1. I compute the following statistice for the overall merged dataset, in particular, for the file `./Preprocessing/Results/tcdb.mtx`.

   |Type of statistics|Value|
   |:---|---:|
   |Number of proteins|12546|
   |Number of features|25704|
   |Number of categories|20|

1. Category information are listed in the table as follows: 

   |Feature prefix|Number of features|Feature type|Version information|Description|
   |:---:|---:|:---:|:---:|:----------|
   |TC__|3145|	TCDB||TCDB classification|
   |TB__|12535|	BLAST||BLAST search|
   |TIProDom__|145|	ProDom|2006.1|ProDom is a comprehensive set of protein domain families automatically generated from the UniProt Knowledge Database.|
   |TIHamap__|209|	HAMAP||High-quality Automated and Manual Annotation of Microbial Proteomes|
   |TISMART__|240|	SMART|6.2|SMART allows the identification and analysis of domain architectures based on Hidden Markov Models or HMMs|
   |TISUPERFAMILY__|512|	SuperFamily|1.75|SUPERFAMILY is a database of structural and functional annotation for all proteins and genomes.|
   |TIPRINTS__|579|	PRINTS|42.0|A fingerprint is a group of conserved motifs used to characterise a protein family|
   |TIPANTHER__|4070|	Panther|9.0|The PANTHER (Protein ANalysis THrough Evolutionary Relationships) Classification System is a unique resource that classifies genes by their functions, using published scientific experimental evidence and evolutionary relationships to predict function even in the absence of direct experimental evidence.|
   |TIGene3D__|611|	Gene3d|3.5.0|Structural assignment for whole genes and genomes using the CATH domain structure database|
   |TIPIRSF__|283|	PIRSF|3.01|The PIRSF concept is being used as a guiding principle to provide comprehensive and non-overlapping clustering of UniProtKB sequences into a hierarchical order to reflect their evolutionary relationships.|
   |TIPfam__|2025|	PfamA|27.0|A large collection of protein families, each represented by multiple sequence alignments and hidden Markov models (HMMs)|
   |TIProSiteProfiles__|282|	PrositeProfiles||PROSITE consists of documentation entries describing protein domains, families and functional sites as well as associated patterns and profiles to identify them|
   |TITIGRFAM__|769|	TIGRFAM|15.0|TIGRFAMs are protein families based on Hidden Markov Models or HMMs|
   |TIProSitePatterns__|285|	PrositePatterns||PROSITE consists of documentation entries describing protein domains, families and functional sites as well as associated patterns and profiles to identify them|
   |TICoils__|1|	Coils|2.2|Prediction of Coiled Coil Regions in Proteins|
   |TITMHMM__|1|	TMHMM| 2.0| Prediction of transmembrane helices in proteins| 
   |TIPhobius__|7|	Phobius |1.01|A combined transmembrane topology and signal peptide predictor|
   |TISignalP_GRAM_NEGATIVE__|2|	SignalP_GRAM_NEGATIVE |4.0|SignalP (organism type gram-negative prokaryotes) predicts the presence and location of signal peptide cleavage sites in amino acid sequences for gram-negative prokaryotes|
   |TISignalP_EUK__|2|	SignalP_EyUK|4.0|SignalP (organism type eukaryotes) predicts the presence and location of signal peptide cleavage sites in amino acid sequences for eukaryotes.|
   |TISignalP_GRAM_POSITIVE__|1|	SignalP_GRAM_POSITIVE |4.0|SignalP (organism type gram-positive prokaryotes) predicts the presence and location of signal peptide cleavage sites in amino acid sequences for gram-positive prokaryotes|
 







