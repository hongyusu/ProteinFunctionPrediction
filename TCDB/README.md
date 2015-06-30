Readme file for th directory TCDB

Directory source:  ------------------

- do.TCDB.R : R script file used to generate both the annotation and the tree structure of the taxonomy.
It uses the library files TCDB.R and IOgraph.R to parse the source files of the TCDB, and construct both the annotation and the tree of the TCDB taxonomy. 

- TCDB.R: R library to process  the source files of the TCDB
IOgraph.R:  R library to construct graph of class graphNEL (graph package of R) and to transform them in text files.

Directory Data:  -------------

Note: all the data refer to the tcdb file (7 june 2015) downloaded from the TCDB
(http://www.tcdb.org/public/) 

- tcdb7June2015.txt: original tcdb file downloaded from the TCDB repository  (version 7 june 2015). Note that the two errrors have been fixed: 
The first one is a space after the AC P81694
>gnl|TC-DB|P81694 |8.B.19.2.2 Omega-ctenitoxin-Cs1a OS=Cupiennius salei PE=1 SV=2
The second s the missed protein description field for protein UPI0002B5B01D:
>gnl|TC-DB|UPI0002B5B01D|1.E.49.1.3

- tcdb20June2015.txt: original tcdb file downloaded from the TCDB repository  (version 20 june 2015). The same previous two errors have been fixed.

- tcdb.ann.7june2015.txt: text file including the data extracted from each first row of the FASTA entries of tcdb7June2015.txt

- ann.rda: R binary files containing the full annotation table (a named data frame). Rows are proteins and columns TCDB classes. If i is a protien and j a TCDB class, then ann[i,j]=1 iff protein i is annotated with class j, otherwise ann[i,j]=0. Names of the rows are SwissProt AC, Names of the columns are TCDB classes.

- ann.txt.gz: a gzipped text file with the same logical format of ann.rda. The first row contains the names of the TCDB classes, while the other rows start with the SwissProt AC and continue with the 1/0 vector of the annotations. Values are separated by a space.

- ann1.rda, ann2.rda, ann3.rda, ann4.rda and ann5.rda: the same as ann.rda but incluidng only annotations for the class at level 1 (the most general), 2, 3, 4 and 5 (the leaves).

- ann12.txt.gz, ann123.txt.gz ann1234.txt.gz:  gzipped text files with the annotation restricted respectively to the first 2, 3 and 4 levels.

- edges.txt: text files with the edges of the TCDB tree. Each row corresponds to an edge of the tree with the format:
parent_node  child_node

- tcdb.tree.rda: TCDB full tree as a graph of class graphNEL in compress R binary format.

- tcdb2levels.tree.rda, tcdb3levels.tree.rda, tcdb4levels.tree.rda: the same as tcdb.tree.rda but limited repsectively to the first 2, 3 and 4 levels.
