


#Table of Contents

- [Table of content](#table-of-content)
- [Introduction](#introduction)
- [Data](#data)
    - [Data from Master thesis](#data-from-master-thesis)
    - [Other data](#other-data)
- [Preprocessing](#preprocessing)
    - [Use the data from Master thesis](#use-data-from-master-thesis)
    - [Generate protein data with BLAST and InterProScan](#generate-protein-data-with-blast-and-interproscan)
    - [Data statistics](#data-statistics)
- [Empirical evaluation](#empirical-evaluation)
    - [Support vector machines](#support-vector-machines)
        - [SVM experiment settings](#svm-experiment-settings)
        - [SVM results](#svm-results)
    - [Multiple kernel learning](#multiple-kernel-learning)
        - [MKL experiment settings](#mkl-experiment-settings)
        - [MKL kernel weights](#mkl-kernel-weights)
        - [MKL results](#mkl-results)
    - [Structured output learning](#structured-output-learning)
        - [SOP results](#sop-results)
    - [Max margin regression](#max-margin-regression)
        - [MMR results](#mmr-results)
- [Additional features](#additional-features)
    - [PSSM features generated from CDD database](#pssm-features-generated-from-cdd-database)
    - [PSSM features generated from TCDB](#pssm-features-generated-from-tcdb)
    - [PSSM features generated from TCDB-CDD](#pssm-features-generated-from-tcdb-cdd)
- [Statistics of feature sets](#statistics-of-feature-sets)

# Introduction

For now the project aims to reliably predict the function of the transporter proteins.
The function is defined as TC code following the hierarchical structure of the transporter protein classification system.
The hierarchical structure of the classification system has five level. We aim to predict the first four level as the fifth level is the very specific classification.
In addition to the transporter proteins documented in TCDB, we also collect proteins from UniProt.
Uniprot proteins have the following features:

   1. Gene Ontology
   2. Protein Family
   3. _BLAST_ score with UniProt
   4. Taxonomy in NCBI

For TCDB proteins we extract features of the following two categorises

   1. _BLAST_ score with TCDB
   2. Many InterProScan features

# Data

## Data from Master thesis
 
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

## Other data

We extract protein classification data from TCDB database.
As the intersection of the protein data listed above and the ones in TCDB is very small we compute protein features via _BLAST_ and InterProScan.

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


1. [_BLAST_ with TCDB](http://hongyusu.github.io/lessons/2015/06/16/ncbi-blast-installation-and-running-in-parallel/)

   1. Protein sequences are aligned with themselves by running _BLAST_ algorithms.
   1. This procedure will genrate a pairwise similarity matrix.
   1. Instruction for installing and running _BLAST_ can be found from [my blog post](http://hongyusu.github.io/lessons/2015/06/16/ncbi-blast-installation-and-running-in-parallel/). 
   1. In particular, after removing some replicated proteins, there are 12515 protein left in TCDB which will be used to build a TCDB _BLAST_ database.
   1. The cleaned TCDB data file is located in `./Data/tcdb`.
   1. For the _BLAST_ search, we obtain all hits with e-value below 0.01. 
   1. We use _BLAST_ score as similary measure between pair of proteins.
   1. Some statistics about the TCDB _BLAST_ features are shown in the following table

      |Type of Data|Number of items|
      |---:|---:|
      |Protein|12515|
      |TCDB _BLAST_ feature|12515|

   1. Data file for TCDB _BLAST_ feature is located as `./Data/tcdbblast`.

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

      |Tool|Version|Information|
      |:---|:---:|:---|
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
      |SignalP GRAM NEGATIVE |4.0|SignalP (organism type gram-negative prokaryotes) predicts the presence and location of signal peptide cleavage sites in amino acid sequences for gram-negative prokaryotes|
      |SignalP EUK |4.0|SignalP (organism type eukaryotes) predicts the presence and location of signal peptide cleavage sites in amino acid sequences for eukaryotes.|
      |SignalP GRAM POSITIVE |4.0|SignalP (organism type gram-positive prokaryotes) predicts the presence and location of signal peptide cleavage sites in amino acid sequences for gram-positive prokaryotes|
   
   1. Note that the last five tools and Panthon database are installed into InterProScan manually.
   1. It is not necessary to perform again the scanning with InterProScan for all TCDB sequences as most of the TCDB sequences already have UniProt accession number. Therefore, we depend on the lookup service provided by InterProScan in order to directly extract the sequence features from the database.
   1. In addition to direct extraction, protein sequences that is not known to InterProScan are scanned.
   1. Interproscan results is located as `./Data/tcdbips`. The file follows the structure described in the following table

      |Column|Description|
      |:---:|:---|
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


# Preprocessing

## Use the data from Master thesis

1. The first strategy we used is to merge the protein data from the Master thesis and from TCDB database to find an intersection of proteins with both various features and classification information in TCDB.
1. However, we found out that the intersection is very small. Only about 1000 proteins from TCDB has feature representations in the Master thesis data.
1. Anywauy, this strategy is briefly illustrated as followings:
   1. Merge datasets from different sources:
   
      1. Merge the following feature types into one matrix
   
         |Data type|#Proteins|#Features|
         |:----|:----:|:----:|
         |matgoBP|101422|12891|
         |matgoCC|101422|1670|
         |matgoMF|101422|4816|
         |matblastcompressed|56838|12646|
         |matpfam|100589|7341|
         |mattaxo|104116|3004|
         |TCDB|12516|9456|
   
      2. A big global matrix is computed by concatenating the matrices of protein-GO, protein-Blast, protein-Ffam, protein-taxonomy, and protein-TCDB, and protein-TCDBblast.
   
         1. The number of proteins and the number of features in the union of the collection of matrices are shown in the following table.
   
         2. The number of proteins and the number of features in the intersection of the collection of matrics are shown in the following table. Notice that a protein will present in the interection matrix if it has features in GO/_BLAST_/Pfam/Taxonomy categories. 
   
            |Type|#Proteins|#Features|
            |:----|:----:|:----:|
            |Union|123619|64328|
            |Intersection|1336|64328|
   
         3. Different type of fetures are annotated in `.collab` according to the following table
   
            |Feature name|Prefix|
            |:---|:---:|
            |Gene ontology: biological process|GB|
            |Gene ontology: cellular component|GC|
            |Gene ontology: molecular function|GM|
            |Protein family|PF|
            |_BLAST_|MB|
            |Taxonomy|MT|
            |TCDB classification|TC|
            |TCDB _BLAST_|TB|

## Generate protein data with BLAST and InterProScan

1. Realizing that I cannot rely on the data used in the Master thesis, I directly work on proteins from TCDB. In particular, I compuate various protein features via running _BLAST_ search and InterProScan.
  
1. First I remove duplicated proteins from the transporter protein classification database (TCDB), particularly, by analyzing the sequence-classification data file.
      
   NOTE: In this way you removed the annotations for proteins having multiple annotation paths. These are 29:
   
   |AC|TC|
   |:---:|:---|
   |D4ZJA6|1.A.30.1.5|
   |D4ZJA6|1.A.30.1.6|
   |O24303|1.A.18.1.1|
   |O24303|3.A.9.1.1|
   |O34840|2.A.19.2.7|
   |O34840|2.A.19.2.11|
   |P0AAW9|8.A.50.1.1|
   |P0AAW9|2.A.6.2.2|
   |P0C1S5|9.A.39.1.3|
   |P0C1S5|9.A.39.1.2|
   |P18409|1.B.33.3.1|
   |P18409|1.B.8.6.1|
   |P23644|3.A.8.1.1|
   |P23644|1.B.8.2.1|
   |P25568|2.A.1.24.1|
   |P25568|9.A.15.1.1|
   |P28795|9.A.17.1.1|
   |P28795|3.A.20.1.5|
   |P29340|3.A.20.1.1|
   |P29340|3.A.20.1.5|
   |P34230|3.A.1.203.2|
   |P34230|3.A.1.203.6|
   |P94360|3.A.1.1.26|
   |P94360|3.A.1.1.34|
   |Q03PY5|3.A.1.28.2|
   |Q03PY5|3.A.1.26.9|
   |Q03PY7|3.A.1.28.2|
   |Q03PY7|3.A.1.26.9|
   |Q07418|9.A.17.1.1|
   |Q07418|3.A.20.1.5|
   |Q15049|9.B.129.1.1|
   |Q15049|2.A.1.76.1|
   |Q55JG4|9.B.178.1.5|
   |Q55JG4|9.B.178.1.6|
   |Q6GHV7|9.A.39.1.1|
   |Q6GHV7|9.A.39.1.2|
   |Q6GUB0|2.A.88.1.1|
   |Q6GUB0|3.A.1.25.1|
   |Q72L52|3.A.1.1.24|
   |Q72L52|3.A.1.1.25|
   |Q8EAG6|1.A.30.1.5|
   |Q8EAG6|1.A.30.1.6|
   |Q8KQR1|9.A.39.1.4|
   |Q8KQR1|9.A.39.1.2|
   |Q99257|1.I.1.1.1|
   |Q99257|3.A.22.1.1|
   |Q9FBS5|3.A.1.1.42|
   |Q9FBS5|3.A.1.1.43|
   |Q9FBS6|3.A.1.1.42|
   |Q9FBS6|3.A.1.1.43|
   |Q9FBS7|3.A.1.1.42|
   |Q9FBS7|3.A.1.1.43|
   |Q9L0Q1|3.A.1.1.33|
   |Q9L0Q1|3.A.1.1.36|
   |Q9RL01|2.A.1.72.1|
   |Q9RL01|2.A.1.15.15|
   |Q9Y3Q4|1.A.1.5.10|
   |Q9Y3Q4|1.A.1.5.11|


   If we consider only the annotation till to the fourth level we have only 13 proteins with multiple annotated paths, but in this way we miss (considering annotations from the first to the fourth level) 41 annotations. To my opinion it is not a good idea to eliminate such annotations. Considering that in practice there are only a few multiple paths, we can ignore multiple paths in our predictions, but without removing them from the data. You can recover the full TCDB annotations using the file tcdb.1 instead of tcdb in the Data directory.

   The TCDB annotation matrix, including all the duplicated path annotations till to the fourth level of the TCDB is available in Preprocessing/Results/tcdb1.annotations.levels1234.txt.gz.
   This gzipped text file has Protein AC on rows (12546 AC) and 3145 TCDB classes on columns. This is a 0/1 dense matrix: the entry (i,j) is equal to 1 means that protein i is annotated with TCDB class j, otherwise (i,j) = 0.


1. Then I run _BLAST_ search and InterProScan for all preprocessed proteins.
1. Merge TCDB classification (protein labels), TCDB _BLAST_ features, and TCDB InterProScan features.
1. Make data matrices of different types, e.g., different feature matrices and label matrix.
   1. In particular, _BLAST_ features use real number (_BLAST_ score), other InterProScan feature use integer number as count
1. Important scripts and result files are listed as follows.

   ```
   Preprocessing
   |---Bins
       |---process_tcdb.py        # process original TCDB database (remove duplication ect)
       |---merge_tcdb_blast_and_ips.py          # merge TCDB blast, ips and classfiication data
       |---run_blast.sh           # run _BLAST_ search
       |---run_interproscan.sh    # run interproscan search to generate protein features
       |---separate_different_features.py # generate feature matrices of different types
   |---Results
       |---tcdbdata               # merged data in sparse matrix format: 'protein name' 'feature name' 'value' 
       |---tcdbdata.collab        # feature names
       |---tcdbdata.rowlab        # protein names
       |---tcdbdata.mtx           # sparse data matrix with format 'protein id' 'feature id' 'value'
		  |---tcdb1.annotations.gz   # dense matrix (text file gzipped) with Swissprot AC on rows and TCDB classes on columns. 
		                             # Entry (i,j) of the matrix is 1 if protein i is annotated to TC class j, otherwise (i,j) = 0
									 # this matrix includes all the annotations (including multiple paths) obtained from the file tcdb.1 in the Data directory.
   Experiments
   |---Data
       |---tcdb.prefix       # data matrices of different type, where type information are explained in the section of Data statistics.
       |---README.md         # read me file for experimental data
       |---tcdb.collab       # feature names
       |---tcdb.rowlab       # protein names
   |---Data.tar.gz           # compressed Data files, including files in `./Data` folder
   ```
 
## Data statistics

1. I compute the following statistice for the overall merged dataset, in particular, for the file `./Preprocessing/Results/tcdb.mtx`.

   |Type of statistics|Value|
   |:---|:---:|
   |Number of proteins|12546|
   |Number of features|25704|
   |Number of categories|20|

1. Category information are listed in the table as follows: 

   |Prefix|Size|Feature|Version | Feature description|
   |:---|:---:|:---|:---:|:----------|
   |TC__|3145|	TCDB||TCDB classification|
   |TB__|12535|	_BLAST_||_BLAST_ search|
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
   |TISignalP_ GRAM_NEGATIVE__|2|	SignalP GRAM NEGATIVE |4.0|SignalP (organism type gram-negative prokaryotes) predicts the presence and location of signal peptide cleavage sites in amino acid sequences for gram-negative prokaryotes|
   |TISignalP_ EUK__|2|	SignalP EyUK|4.0|SignalP (organism type eukaryotes) predicts the presence and location of signal peptide cleavage sites in amino acid sequences for eukaryotes.|
   |TISignalP_ GRAM_POSITIVE__|1|	SignalP GRAM POSITIVE |4.0|SignalP (organism type gram-positive prokaryotes) predicts the presence and location of signal peptide cleavage sites in amino acid sequences for gram-positive prokaryotes|
 




# Empirical evaluation 

## Support vector machines

In this section, we test the classification performance on transporter classification (TC) based on different input feature maps as discussed in the previous section. 

### SVM experiment settings

1. Linear SVM is used as the baseline learner. We use a SVM implementation from [libSVM](https://www.csie.ntu.edu.tw/~cjlin/libsvm/).
1. We select for each input feature map a SVM margin slack (C) parameter from the set {0.01,0.1,1,10,100}.
1. Parameter selection is baed on a random selection of 5000 proteins from the original dataset.
1. After parametere selection, the best SVM C parameter is applied to both training and test.
1. Experiment results are reported from a five fold cross validation procedure. We randomly divide examples into five disjoin set of equal size. In each iteration, we use one set for testing and the rest for training. The same procedure is then repeated five times.
1. We report the following metrics to measure the performance of the classifier including AUC, accuracy, F1, precision, and recall. The scores are computed by pooling all microlabels.

### SVM results

1. Preliminary experimental results are shown in the following table

   | Input feature | AUC | Accuracy | F1 | Precision | Recall |
   |:--:|:--:|:--:|:--:|:--:|:--:|
   |../Data/tcdb.TB         |0.9641|0.9992|0.7445|0.9786|0.6008|
   |../Data/tcdb.TICoils    |0.8541|0.9964|0.0356|0.0380|0.0336|
   |../Data/tcdb.TIGene3D   |0.8815|0.9881|0.0403|0.0240|0.1266|
   |../Data/tcdb.TIHamap    |0.8691|0.9981|0.0553|0.9498|0.0285|
   |../Data/tcdb.TIPANTHER  |0.9081|0.9981|0.4240|0.5239|0.3562|
   |../Data/tcdb.TIPfam     |0.9415|0.9978|0.3822|0.4201|0.3506|
   |../Data/tcdb.TIPhobius  |0.8991|0.9964|0.1174|0.1130|0.1220|
   |../Data/tcdb.TIPIRSF    |0.8743|0.9981|0.1118|0.9687|0.0593|
   |../Data/tcdb.TIPRINTS   |0.8788|0.9979|0.1369|0.3550|0.0848|
   |../Data/tcdb.TIProDom   |0.8708|0.9981|0.0345|0.9884|0.0176|
   |../Data/tcdb.TIProSitePatterns|0.8672|0.9870|0.0301|0.0176|0.1018|
   |../Data/tcdb.TIProSiteProfiles|0.8783|0.9979|0.1560|0.3745|0.0985|
   |../Data/tcdb.TISignalP_ EUK    |0.8596|0.9899|0.0109|0.0068|0.0283|
   |../Data/tcdb.TISignalP_ GRAM_NEGATIVE|0.8677|0.9979|0.0362|0.2543|0.0195|
   |../Data/tcdb.TISignalP_ GRAM_POSITIVE|0.8724|0.9980|0.0413|0.5434|0.0214|
   |../Data/tcdb.TISMART      |0.8732|0.9979|0.0715|0.2742|0.0411|
   |../Data/tcdb.TISUPERFAMILY|0.8851|0.9975|0.1486|0.2275|0.1104|
   |../Data/tcdb.TITIGRFAM    |0.8819|0.9977|0.2226|0.3421|0.1650|
   |../Data/tcdb.TITMHMM      |0.8694|0.9975|0.0068|0.0153|0.0044|


1. ROC curve is shown as 
  
   ![alt text](https://github.com/aalto-ics-kepaco/ProteinFunctionPrediction/blob/master/Experiments/PlotsSVM/auc.jpg)

## Multiple kernel learning

In stead of predicting the transporter classification (TC) with single feature map as studied in the previous section, we aim to combine those 19 different feature maps with multiple kernel learning approaches.

### MKL experiment settings

1. We compute an input base kernel (gram matrix) for each individual feature map. In particular, each base kenrel is a linear kernel on the original feature map.
1. We compute a linear output kernel for the output multilabels. 
1. Three multiple kernel learning approaches are applied to combine these 19 base kernels including
   1. `UNIMKL` which computes a unifom combination of based kenrels
   1. `ALIGN` which aligns each input kernel with the output kernel, then combines all based kernels according to the alignment scores
   1. `ALIGNF` which maximizes the alignment score between the output kernel and a convex combination of all input kernels
1. Support Vector Machines are used to build the classification model. In particular, we used a LibSVM version with precomputed kernel.
1. We select SVM margin slack parameter (C) based on a random selection of 5000 examples. Best C is selected from the set {0.01,0.1,1,10,100}.
1. After parameter selection, best C parameter is used for training and prediction.
1. Experiment results are reported from a five fold cross validation procedure. We randomly divide examples into five disjoin set of equal size. In each iteration, we use one set for testing and the rest for training. The same procedure is then repeated five times.
1. We report the following metrics to measure the performance of the classifier including AUC (area under the curve), AUPRC (area under the precision-recall curve), accuracy, F1, precision, and recall. The scores are computed by pooling all microlabels. In addition, precision, recall, and accuracy are computed with a threshold 0.5 to binarize all real valued predictions.

### MKL kernel weights 

1. Kernel weights computed from different multiple kernel learning approaches are listed in the following table
 
   |MKL|tcdb.TB|tcdb.TICoils|tcdb.TIGene3D|tcdb.TIHamap|tcdb.TIPANTHER|tcdb.TIPfam|tcdb.TIPhobius|tcdb.TIPIRSF|tcdb.TIPRINTS|tcdb.TIProDom|tcdb.TIProSitePatterns|tcdb.TIProSiteProfiles|tcdb.TISignalP_EUK|tcdb.TISignalP_GRAM_NEGATIVE|tcdb.TISignalP_GRAM_POSITIVE|tcdb.TISMART|tcdb.TISUPERFAMILY|tcdb.TITIGRFAM|tcdb.TITMHMM|
   |:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:---:|
   | UNIMKL |0.05|0.05|0.05|0.05|0.05|0.05|0.05|0.05|0.05|0.05|0.05|0.05|0.05|0.05|0.05|0.05|0.05|0.05|0.05|
   | ALIGN  |0.15|0.01|0.22|0.02|0.19|0.10|0.23|0.04|0.07|0.01|0.03|0.07|0.06|0.06|0.05|0.03|0.17|0.05|0.23|
   | ALIGNF |0.00|0.00|0.09|0.14|0.37|0.00|0.00|0.31|0.00|0.86|0.00|0.00|0.04|0.05|0.01|0.00|0.00|0.00|0.00|

1. In addition, kernel weights are shown in the following bar plot

   ![alt text](https://github.com/aalto-ics-kepaco/ProteinFunctionPrediction/blob/master/Experiments/PlotsMKL/kernel_weights.jpg)

### MKL results

1. Prediction performances of three multiple kernel learning approaches are listed in the following table in which all combined kernel are centered and * corresponds to additional operation on the combined kernel `normalization->centering`.

   |Kernel function| Input feature | AUC | Accuracy | F1 | Precision | Recall | Multilabel Accuracy |
   |:--:           |:--:|:--:|--:|:--:|:--:|:--:|:--:|:--:|
   |Linear         |UNIMKL*| 0.9851 | 0.9989 | 0.6826 | 0.8364 | 0.5766 | 0.2380 
   |Linear         |ALIGN* | 0.9889 | 0.9991 | 0.7463 | 0.8662 | 0.6555 | 0.3179
   |Linear         |ALIGNF*| 0.9878 | 0.9993 | 0.7918 | 0.8885 | 0.7140 | 0.4016 

1. In addition, we use Guassian kenrel on all three computed kernels, the corresponding prediction performance is shown in the following table. 

   |Kernel function| Input feature | AUC | Accuracy | F1 | Precision | Recall | Multilabel Accuracy |
   |:--:           |:--:|:--:|--:|:--:|:--:|:--:|:--:|:--:|
   |Gaussian       |UNIMKL*| 0.8990 | 0.9984 | 0.3172 | 0.9786 | 0.1893 | 0.1248 
   |Gaussian       |ALIGN* | 0.8976 | 0.9984 | 0.3077 | 0.9818 | 0.1825 | 0.1272
   |Gaussian       |ALIGNF*| 0.8902 | 0.9983 | 0.2364 | 0.9834 | 0.1343 | 0.0972 



## Structured output learning

### SOP results

1. Prediction performance of the developed structured output prediction method is shown in the following table. In particular, kernels are computed from multiple kernel learning approaches.

   |Kernel function| Input feature | AUC | Microlabel Accuracy | F1 | Precision | Recall | Multilabel Accuracy | 
   |:--:           |:--:|:--:|--:|:--:|:--:|:--:|:--:|:---:|
   |Linear         |UNIMKL*| NA | 0.9993 | 0.7173 | 0.7173 | 0.7173 | 0.5513 
   |Linear         |ALIGN* | NA | 0.9994 | 0.7711 | 0.7711 | 0.7711 | 0.5874 
   |Linear         |ALIGNF*| NA | 0.9995 | 0.8045 | 0.8045 | 0.8045 | 0.6365 

2. Predidction performance of the developed structured output prediction model with additional Gaussian kernels on kernel matrices that are computed from multiple kernel learning approaches.

   |Kernel function| Input feature | AUC | Microlabel Accuracy | F1 | Precision | Recall | Multilabel Accuracy | 
   |:--:           |:--:|:--:|--:|:--:|:--:|:--:|:--:|:---:|
   |Gaussian       |UNIMKL*| NA | 0.9995 | 0.7992| 0.7992| 0.7992 | 0.6428 
   |Gaussian       |ALIGN* | NA | 0.9996 | 0.8284| 0.8284| 0.8284 | 0.6856 
   |Gaussian       |ALIGNF*| NA | 0.9996 | 0.8524| 0.8524| 0.8524 | 0.7281 


## Max margin regression

### MMR results

1. Prediction performance of MMR is shown in the following table. In particular, kernels are computed directly from multiple kernel learning approaches.

   |Kernel function| Input feature | AUC | Microlabel Accuracy | F1 | Precision | Recall | Multilabel Accuracy | 
   |:--:           |:--:|:--:|--:|:--:|:--:|:--:|:--:|:---:|
   |Linear         |UNIMKL*| NA | NA | 0.3512 | 0.3512 | 0.3512 | 0.0690 
   |Linear         |ALIGN* | NA | NA | 0.3387 | 0.3387 | 0.3387 | 0.0587 
   |Linear         |ALIGNF*| NA | NA | 0.5012 | 0.5012 | 0.5012 | 0.2095 

2. Predidction performance of MMR with additional Gaussian kernels on kernel matrices that are computed from multiple kernel learning approaches.

   |Kernel function| Input feature | AUC | Microlabel Accuracy | F1 | Precision | Recall | Multilabel Accuracy | 
   |:--:           |:--:|:--:|--:|:--:|:--:|:--:|:--:|:---:|
   |Gaussian       |UNIMKL*| NA | NA | 0.7987 | 0.7987 | 0.7987 | 0.6409 
   |Gaussian       |ALIGN* | NA | NA | 0.8296 | 0.8296 | 0.8296 | 0.6828 
   |Gaussian       |ALIGNF*| NA | NA | 0.8537 | 0.8537 | 0.8537 | 0.7272 

## Additional features

### PSSM features generated from CDD database 

1. There are many public databases which contains conserved protein domain information in position specific scoring matrix PSSM format. 
1. This section describes how to compute position specific scoring matrix PSSM features from public conserved domain databases CDD.
1. Download CDD database source files from [NCBI FTP server](ftp://ftp.ncbi.nih.gov/pub/mmdb/cdd//cdd.tar.gz).
1. Download CDD database version file from [NCBI FTP server](ftp://ftp.ncbi.nih.gov/pub/mmdb/cdd//cdd.info).
1. Download PSSM version file from [NCBI FTP server](ftp://ftp.ncbi.nih.gov/pub/mmdb/cdd//cdd.versions).
1. The following table shows the statistics and version information of all databases in CDD.

   |Database|Number of PSSM models|Version|
   |:---:|---:|---:|
   |CDD  |47363| v3.14|
   |Pfam |14831 | v27.0|
   |COG|4825| v1.0 |
   |KOG|4875| v1.0 |
   |SMART|1013|v6.0|
   |PRK|10885|v6.9|
   |TiGRFAM|4488|v15.0|
   |CDD NCBI|11273||

1. Build local CDD databases from different source files using NCBI Blast+ tool according to the following commands.

   `../makeprofiledb -title SMART     -in Smart.pn -out Smart -threshold 9.82 -scale 100.0 -dbtype rps -index true`

   `../makeprofiledb -title Pfam      -in Pfam.pn -out Pfam -threshold 9.82 -scale 100.0 -dbtype rps -index true`

   `../makeprofiledb -title COG       -in Cog.pn -out Cog -threshold 9.82 -scale 100.0 -dbtype rps -index true`

   `../makeprofiledb -title KOG       -in Kog.pn -out Kog -threshold 9.82 -scale 100.0 -dbtype rps -index true`

   `../makeprofiledb -title CDD_NCBI  -in Cdd_NCBI.pn -out Cdd_NCBI -threshold 9.82 -scale 100.0 -dbtype rps -index true`

   `../makeprofiledb -title PRK       -in Prk.pn -out Prk -threshold 9.82 -scale 100.0 -dbtype rps -index true`

   `../makeprofiledb -title Tigr      -in Tigr.pn -out Tigr -threshold 9.82 -scale 100.0 -dbtype rps -index true`

1. A CDD database covering all sources can be built with the following command 

   `../makeprofiledb -title CDD       -in Cdd.pn -out Cdd -threshold 9.82 -scale 100.0 -dbtype rps -index true`

1. Once the databases are ready, BLAST search can be performed with `rpsblast` with the following command (e.g., search against SMART CDD).

   `../Blast/ncbi-blast-2.2.31+/bin/rpsblast  -evalue 0.01 -num_threads 4 -outfmt "6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore" -db ../Blast/ncbi-blast-2.2.31+/bin/CDD/SMART -query ../../Data/tcdb -out ../../Data/tcdbrpsSMART `

1. The complete code is available from [my GitHub](https://github.com/hongyusu/ProteinFunctionPrediction/blob/master/Preprocessing/Bins/run_rpsblast.py).

### PSSM features generated from TCDB

1. `psiblast` provides an alternative to search against TCDB database with PSSM features.
1. In particular, each protein sequence is searched against TCDB and a PSSM is computed for this sequence. 
1. After that, the system use constructed PSSM to perform a second search against TCDB.
1. The command to perform `psiblast` search is shown as the following.  

   `../../makeprofiledb -title TCDB201509PSSM -in tcdb201509pssm.pn -out tcdb201509pssm -threshold 9.82 -scale 100.0 -dbtype rps -index true`

1. The complete code is available from [my GitHub](https://github.com/hongyusu/ProteinFunctionPrediction/blob/master/Preprocessing/Bins/run_psiblast.py).

## PSSM features generated from TCDB-CDD

1. As an alterntive, one can search each protein sequence against TCDB and generate a PSSM pattern.
1. With all generate PSSM patterns, one can build a CDD database of TCDB protein sequences.
1. After that, each protein sequence is search against the CDD dataabse of TCDB protein sequences.
1. The complete code is available from [my GitHub](https://github.com/hongyusu/ProteinFunctionPrediction/blob/master/Preprocessing/Bins/run_rpsblast.py).
1. Statistics of CDD database of TCDB sequences is shown in the following table.

   |Database|Number of PSSM models|Version|
   |:---:|---:|---:|
   |CDD-TCDB  |12540| 201509 version of TCDB|

# Statistics of feature sets

1. The following table shows the statistics of features computed for TCDB prediction tasks.

   |Feature set| Number of features|
   |:---|---:|
   |TB | 12535 | 
   |TC | 3145 | 
   |TICoils | 1 | 
   |TIGene3D | 611 | 
   |TIHamap | 209 | 
   |TIPANTHER | 4070 | 
   |TIPfam | 2025 | 
   |TIPhobius | 7 | 
   |TIPIRSF | 283 | 
   |TIPRINTS | 579 | 
   |TIProDom | 145 | 
   |TIProSitePatterns | 285 | 
   |TIProSiteProfiles | 282 | 
   |TISignalPEUK | 2 | 
   |TISignalP_GRAM_NEGATIVE | 2 | 
   |TISignalP_GRAM_POSITIVE | 1 | 
   |TISMART | 240 | 
   |TISUPERFAMILY | 512 | 
   |TITIGRFAM | 769 | 
   |TITMHMM | 1 | 
   |TPSI | 12540 | 
   |TRPSCDD | 10727 | 
   |TRPSCDDNCBI | 4265 | 
   |TRPSCOG | 1739 | 
   |TRPSKOG | 2066 | 
   |TRPSPFAM | 3048 | 
   |TRPSPRK | 3374 | 
   |TRPSSMART | 394 | 
   |TRPSTCDB201509PSSM | 12531 | 
   |TRPSTIGR | 1561 | 


   | MMCRF | Kernel | AUC | Microlabel Accuracy | F1 | Precision | Recall | Multilabel Accuracy | 
   |:--:|:--:|--:|:--:|:--:|:--:|:--:|:---:|
   |Linear | UNIMKL | NaN | 0.9995 | 0.7957 | 0.7957 | 0.7957 | 0.6176
   |Linear | ALIGN  | NaN | 0.9995 | 0.8174 | 0.8174 | 0.8174 | 0.6334
   |Linear | ALIGNF | NaN | 0.9996 | 0.8240 | 0.8240 | 0.8240 | 0.6426
   |Gaussian |UNIMKL | NaN | 0.9996 | 0.8369 | 0.8369 | 0.8369 | 0.6977
   |Gaussian |ALIGN  | NaN | 0.9996 | 0.8615 | 0.8615 | 0.8615 | 0.7421

   | MMR | Kernel | AUC | Microlabel Accuracy | F1 | Precision | Recall | Multilabel Accuracy | 
   |:--:|:--:|--:|:--:|:--:|:--:|:--:|:---:|
   |Linear | UNIMKL  | NaN | 0.9995 | 0.4332 | 0.4332 | 0.4332 | 0.1198
   |Linear | ALIGN   | NaN | 0.9995 | 0.4384 | 0.4384 | 0.4384 | 0.1241
   |Linear | ALIGNF  | NaN | 0.9996 | 0.4955 | 0.4955 | 0.4955 | 0.1752
   |Gaussian |UNIMKL | NaN | 0.9996 | 0.8354 | 0.8354 | 0.8354 | 0.6811
   |Gaussian |ALIGN  | NaN | 0.9996 | 0.8550 | 0.8550 | 0.8550 | 0.7191
   |Gaussian |ALIGNF | NaN | 0.9996 | 0.8463 | 0.8463 | 0.8463 | 0.6839

   | MKL | Kernel | AUC | Microlabel Accuracy | F1 | Precision | Recall | Multilabel Accuracy | 
   |:--:|:--:|--:|:--:|:--:|:--:|:--:|:---:|
   |Linear | KUNIMKL | 0.9942 | 0.9995 | 0.8485 | 0.9344 | 0.7770 | 0.5327
   |Linear | KALIGN  | 0.9946 | 0.9995 | 0.8621 | 0.9377 | 0.7978 | 0.5484
   |Linear | KALIGNF | 0.9928 | 0.9996 | 0.8822 | 0.9485 | 0.8245 | 0.6048




   |MMCRF| Input feature | AUC | Microlabel Accuracy | F1 | Precision | Recall | Multilabel Accuracy | 
   |:--:           |:--:|:--:|--:|:--:|:--:|:--:|:--:|:---:|
   |Linear         |UNIMKL| NA | 0.9993 | 0.7173 | 0.7173 | 0.7173 | 0.5513 
   |Linear         |ALIGN | NA | 0.9994 | 0.7711 | 0.7711 | 0.7711 | 0.5874 
   |Linear         |ALIGNF| NA | 0.9995 | 0.8045 | 0.8045 | 0.8045 | 0.6365 
   |Gaussian       |UNIMKL| NA | 0.9995 | 0.7992| 0.7992| 0.7992 | 0.6428 
   |Gaussian       |ALIGN | NA | 0.9996 | 0.8284| 0.8284| 0.8284 | 0.6856 
   |Gaussian       |ALIGNF| NA | 0.9996 | 0.8524| 0.8524| 0.8524 | 0.7281 


   |MMR| Input feature | AUC | Microlabel Accuracy | F1 | Precision | Recall | Multilabel Accuracy | 
   |:--:           |:--:|:--:|--:|:--:|:--:|:--:|:--:|:---:|
   |Linear         |UNIMKL| NA | NA | 0.3512 | 0.3512 | 0.3512 | 0.0690 
   |Linear         |ALIGN | NA | NA | 0.3387 | 0.3387 | 0.3387 | 0.0587 
   |Linear         |ALIGNF| NA | NA | 0.5012 | 0.5012 | 0.5012 | 0.2095 
   |Gaussian       |UNIMKL| NA | NA | 0.7987 | 0.7987 | 0.7987 | 0.6409 
   |Gaussian       |ALIGN | NA | NA | 0.8296 | 0.8296 | 0.8296 | 0.6828 
   |Gaussian       |ALIGNF| NA | NA | 0.8537 | 0.8537 | 0.8537 | 0.7272 

   |Kernel function| Input feature | AUC | Accuracy | F1 | Precision | Recall | Multilabel Accuracy |
   |:--:           |:--:|:--:|--:|:--:|:--:|:--:|:--:|:--:|
   |Linear         |UNIMKL| 0.9851 | 0.9989 | 0.6826 | 0.8364 | 0.5766 | 0.2380 
   |Linear         |ALIGN | 0.9889 | 0.9991 | 0.7463 | 0.8662 | 0.6555 | 0.3179
   |Linear         |ALIGNF| 0.9878 | 0.9993 | 0.7918 | 0.8885 | 0.7140 | 0.4016 
   |Gaussian       |UNIMKL| 0.8990 | 0.9984 | 0.3172 | 0.9786 | 0.1893 | 0.1248 
   |Gaussian       |ALIGN | 0.8976 | 0.9984 | 0.3077 | 0.9818 | 0.1825 | 0.1272
   |Gaussian       |ALIGNF| 0.8902 | 0.9983 | 0.2364 | 0.9834 | 0.1343 | 0.0972 


