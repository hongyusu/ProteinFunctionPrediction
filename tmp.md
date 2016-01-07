
# Introduction

The final goal of this project is to reliably predict the protein functions in terms of transporter function classification.
The fucntion is defined as a TC code following the hierarchical structure (a tree) of the transporter protein classification system.
In particular, there are five levels in the hierarchical classification system of which we aim to prediction the first four levels.
This is due to the fact that the functional annotations on the fifth level are very specific. 

We collection over 12,000 protein sequences from TCDB database and generate for each sequence a varity of features of the following three categories

1. BLAST feature
1. InterProScan features
1. Position specific scoring matrix features






# Data

## TCDB data

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



# Preprocessing

1. First I remove duplicated proteins from the transporter protein classification database (TCDB), particularly, by analyzing the sequence-classification data file.
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

# Feature generation

## BLAST features

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


## Interproscan features

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

## Data statistics of BLAST and IPS featuers

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



## PSSM features 

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




## Statistics of feature sets

The following table shows the statistics of features computed for TCDB prediction tasks.

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



# Empirical evaluation 

## Support vector machines (SVM)

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

   | Input feature | AUC | Microlabel Accuracy | F1 | Precision | Recall | Multilabel Accuracy |
   |:--:|:--:|:--:|:--:|:--:|:--:|:--:|
   |TB                      |0.8705|0.9980|0.0023|1.0000|0.0012|0.0000|
   |TICoils                 |0.8705|0.9980|0.0023|1.0000|0.0012|0.0000|
   |TIGene3D                |0.8729|0.9982|0.2151|0.9255|0.1217|0.0046|
   |TIHamap                 |0.8714|0.9980|0.0122|0.8896|0.0061|0.0000|
   |TIPANTHER               |0.8721|0.9981|0.0335|0.9857|0.0170|0.0000|
   |TIPfam                  |0.8727|0.9981|0.0985|0.6216|0.0535|0.0000|
   |TIPhobius               |0.9048|0.9979|0.2111|0.3945|0.1441|0.0006|
   |TIPIRSF                 |0.8714|0.9980|0.0208|0.9941|0.0105|0.0004|
   |TIPRINTS                |0.8730|0.9981|0.0630|0.9765|0.0325|0.0074|
   |TIProDom                |0.8711|0.9980|0.0036|0.9886|0.0018|0.0000|
   |TIProSitePatterns       |0.8720|0.9981|0.1007|0.9896|0.0531|0.0039|
   |TIProSiteProfiles       |0.8727|0.9982|0.1976|0.9925|0.1097|0.0041|
   |TISignalP_EUK           |0.8714|0.9980|0.0481|0.5812|0.0251|0.0000|
   |TISignalP_GRAM_NEGATIVE |0.8708|0.9980|0.0377|0.6214|0.0194|0.0000|
   |TISignalP_GRAM_POSITIVE |0.8722|0.9980|0.0413|0.5434|0.0214|0.0000|
   |TISMART                 |0.8734|0.9981|0.0933|0.9577|0.0491|0.0015|
   |TISUPERFAMILY           |0.8810|0.9983|0.3264|0.8470|0.2022|0.0076|
   |TITIGRFAM               |0.8721|0.9981|0.0401|0.9861|0.0205|0.0002|
   |TITMHMM                 |0.8706|0.9980|0.1953|0.5192|0.1203|0.0009|
   |TPSI                    |0.8705|0.9980|0.0082|0.9804|0.0041|0.0000|
   |TRPSCDD                 |0.8705|0.9980|0.0023|1.0000|0.0012|0.0000|
   |TRPSCDDNCBI             |0.8710|0.9981|0.0952|0.9635|0.0501|0.0015|
   |TRPSCOG                 |0.8860|0.9982|0.2196|0.9124|0.1248|0.0091|
   |TRPSKOG                 |0.8808|0.9982|0.1956|0.9352|0.1092|0.0142|
   |TRPSPFAM                |0.8715|0.9980|0.0252|0.9968|0.0128|0.0000|
   |TRPSPRK                 |0.8717|0.9981|0.1247|0.7926|0.0677|0.0019|
   |TRPSSMART               |0.8712|0.9981|0.0890|0.9457|0.0467|0.0014|
   |TRPSTCDB201509PSSM      |0.8705|0.9980|0.0023|1.0000|0.0012|0.0000|
   |TRPSTIGR                |0.8728|0.9981|0.1134|0.9888|0.0601|0.0037|

## Multiple kernel learning (MKL)

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
 
 | Base kernel| UNIMKL | ALIGN | ALIGNF |
 |:---:|--:|--:|--:|
 |TB.K                        |0.03 | 0.17 | 0.00|  
 |TICoils.K                   |0.03 | 0.01 | 0.02|  
 |TIGene3D.K                  |0.03 | 0.14 | 0.00|  
 |TIHamap.K                   |0.03 | 0.02 | 0.29|  
 |TIPANTHER.K                 |0.03 | 0.14 | 0.08|  
 |TIPfam.K                    |0.03 | 0.19 | 0.29|  
 |TIPhobius.K                 |0.03 | 0.20 | 0.22|  
 |TIPIRSF.K                   |0.03 | 0.02 | 0.11|  
 |TIPRINTS.K                  |0.03 | 0.02 | 0.01|  
 |TIProDom.K                  |0.03 | 0.01 | 0.14|  
 |TIProSitePatterns.K         |0.03 | 0.09 | 0.00|  
 |TIProSiteProfiles.K         |0.03 | 0.14 | 0.01|  
 |TISignalP_EUK.K             |0.03 | 0.06 | 0.03|  
 |TISignalP_GRAM_NEGATIVE.K   |0.03 | 0.06 | 0.08|  
 |TISignalP_GRAM_POSITIVE.K   |0.03 | 0.05 | 0.00|  
 |TISMART.K                   |0.03 | 0.14 | 0.00|  
 |TISUPERFAMILY.K             |0.03 | 0.16 | 0.11|  
 |TITIGRFAM.K                 |0.03 | 0.04 | 0.06|  
 |TITMHMM.K                   |0.03 | 0.18 | 0.00|  
 |TPSI.K                      |0.03 | 0.24 | 0.20|  
 |TRPSCDD.K                   |0.03 | 0.03 | 0.00|  
 |TRPSCDDNCBI.K               |0.03 | 0.21 | 0.24|  
 |TRPSCOG.K                   |0.03 | 0.24 | 0.64|  
 |TRPSKOG.K                   |0.03 | 0.11 | 0.00|  
 |TRPSPFAM.K                  |0.03 | 0.21 | 0.33|  
 |TRPSPRK.K                   |0.03 | 0.19 | 0.01|  
 |TRPSSMART.K                 |0.03 | 0.14 | 0.08|  
 |TRPSTCDB201509PSSM.K        |0.03 | 0.25 | 0.31|  
 |TRPSTIGR.K                  |0.03 | 0.20 | 0.00|  

1. In addition, kernel weights are shown in the following bar plot

   ![alt text](https://github.com/aalto-ics-kepaco/ProteinFunctionPrediction/blob/master/Experiments/PlotsMKL/kernel_weights.jpg)


### Support vector machine (SVM)

Prediction performances of three multiple kernel learning approaches are listed in the following table in which all combined kernel are `centered->normalized->centered`. In addition, we use Guassian kenrel on all three computed kernels, the corresponding prediction performance is shown in the following table. 

| MKL | Kernel | AUC | Microlabel Accuracy | F1 | Precision | Recall | Multilabel Accuracy | 
|:--:|:--:|--:|:--:|:--:|:--:|:--:|:---:|
|Linear | UNIMKL | 0.9942 | 0.9995 | 0.8485 | 0.9344 | 0.7770 | 0.5327
|Linear | ALIGN  | 0.9946 | 0.9995 | 0.8621 | 0.9377 | 0.7978 | 0.5484
|Linear | ALIGNF | 0.9928 | 0.9996 | 0.8822 | 0.9485 | 0.8245 | 0.6048
|Gaussian | UNIMKL | 0.9303 | 0.9988 | 0.5568 | 0.9619 | 0.3918 | 0.2315
|Gaussian | ALIGN  | 0.9169 | 0.9985 | 0.3938 | 0.9722 | 0.2469 | 0.1595
|Gaussian | ALIGNF | 0.9461 | 0.9990 | 0.6609 | 0.9619 | 0.5034 | 0.3289


### Max-margin conditional random field (MMCRF)

Prediction performance of the developed structured output prediction method is shown in the following table. In particular, kernels are computed from multiple kernel learning approaches. Predidction performance of the developed structured output prediction model with additional Gaussian kernels on kernel matrices that are computed from multiple kernel learning approaches.

| MMCRF | Kernel | AUC | Microlabel Accuracy | F1 | Precision | Recall | Multilabel Accuracy | 
|:--:|:--:|--:|:--:|:--:|:--:|:--:|:---:|
|Linear | UNIMKL | NA | 0.9995 | 0.7957 | 0.7957 | 0.7957 | 0.6176
|Linear | ALIGN  | NA | 0.9995 | 0.8174 | 0.8174 | 0.8174 | 0.6334
|Linear | ALIGNF | NA | 0.9996 | 0.8240 | 0.8240 | 0.8240 | 0.6426
|Gaussian |UNIMKL | NA | 0.9996 | 0.8369 | 0.8369 | 0.8369 | 0.6977
|Gaussian |ALIGN  | NA | 0.9996 | 0.8615 | 0.8615 | 0.8615 | 0.7421
|Gaussian |ALIGNF | NA | 0.9996 | 0.8537 | 0.8537 | 0.8537 | 0.7118


### Max margin regression (MMR)

Prediction performance of MMR is shown in the following table. In particular, kernels are computed directly from multiple kernel learning approaches. Predidction performance of MMR with additional Gaussian kernels on kernel matrices that are computed from multiple kernel learning approaches.

| MMR | Kernel | AUC | Microlabel Accuracy | F1 | Precision | Recall | Multilabel Accuracy | 
|:--:|:--:|--:|:--:|:--:|:--:|:--:|:---:|
|Linear | UNIMKL  | NA | NA | 0.4332 | 0.4332 | 0.4332 | 0.1198
|Linear | ALIGN   | NA | NA | 0.4384 | 0.4384 | 0.4384 | 0.1241
|Linear | ALIGNF  | NA | NA | 0.4955 | 0.4955 | 0.4955 | 0.1752
|Gaussian |UNIMKL | NA | NA | 0.8354 | 0.8354 | 0.8354 | 0.6811
|Gaussian |ALIGN  | NA | NA | 0.8550 | 0.8550 | 0.8550 | 0.7191
|Gaussian |ALIGNF | NA | NA | 0.8463 | 0.8463 | 0.8463 | 0.6839





