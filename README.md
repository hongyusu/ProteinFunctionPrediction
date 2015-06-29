

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
   1. Several InterProScan feature

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
   1. Instruction for installing and running BLAST can be found from [my blog post](http://hongyusu.github.io/lessons/2015/06/16/ncbi-blast-installation-and-running-in-parallel/). 
   1. In particular, after removing some replicated proteins, there are 12515 protein left in TCDB which will be used to build a TCDB BLAST database.
   1. For the BLAST search, we obtain all hits with e-value above 0.01. 
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

   1. Otherwise, original data are located in the directory `./Data/`

## Data preprocessing

1. Scripts:

   ```
   |---Bins
   |   |---process_tcdb.py          process original tcdb database (remove duplication ect)
   |   |---merge_tcdb_blast_and_ips.py          merge tcdb blast, ips and classfiication data
   |---Results
   ```

1. Remove duplication in transporter protein classification database (TCDB) sequence v.s. TC classification file.

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
