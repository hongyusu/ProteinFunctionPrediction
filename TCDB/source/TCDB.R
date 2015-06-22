# library to process TCDB files in text format

library(graph);
library(Rgraphviz);

###### MAIN FUNCTIONS #################################################

# Function to extract annotation data from a TCDB text file.
# Arguments:
# tcdb.file: name of the TCDB file
# file: name of the text file where tcdb entries will be written,  If file="" (def.) no text file is written. The fieelds are separated by tab
# Value:
# A data frame with the following columns:
# AC: SwissProt accession numbr of the protein
# TC: TCDB annotation  
# OS: species
# GN: gene name
# PE:  an integer
# SV:  an integer
do.TCDB <- function(tcdb.file, file="") {
  
  tcdb <- readLines(tcdb.file); 
  SwissProtAC <- extract.SwissProt.AC(tcdb);
  TCDB.code <- extract.TCDB.code (tcdb);  
  prot.names <- extract.protein.descr(tcdb);
  OS <- extract.OS(tcdb);
  GN <- extract.GN(tcdb);
  PE <- extract.PE(tcdb);
  SV <- extract.SV(tcdb); 
  m <- data.frame(AC=SwissProtAC, TC=TCDB.code,  OS=OS, GN=GN, PE=PE, SV=SV, stringsAsFactors=FALSE);
  if (file!="") {
     m2 <- data.frame(AC=SwissProtAC, TC=TCDB.code, DESCR=prot.names, OS=OS, GN=GN, PE=PE, SV=SV,  stringsAsFactors=FALSE);
     write.table(m2, file=file);
  }
  return(m);
}


# Function to extract all the classes from the annotations
# Arg:
# ann: character vector of TCDB anotations in the form V.W.X.Y.Z
# Value:
# character vector collecting all the classes
extract.classes <- function(ann) {
  cl <- character(0);
  ann <- unique(ann);
  n <-length(ann);
  x <- strsplit(ann, "\\.");
  for (i in 1:n) {
     z <- x[[i]];
     y <- z[1];
     cl <- c(cl,y);
     for (j in 2:5) {
        y <- paste0(y, ".", z[j]);
        cl <- c(cl,y);
     }
  }
  cl <- sort(unique(cl));
  return(cl);
}

# Function that returns the TCDB classes by level
# Arg:
# cl : character vector with classes
# Value:
# a list with 5 component: each component i includes the classes beloniging to the ith level.
do.class.by.level <- function(cl) {
   cl.by.hier <- vector("list", 5);

   n.classes <- length(cl);
   x <- strsplit(cl, "\\.");
   for (i in 1:n.classes) {
      level <- length(x[[i]]);
      cl.by.hier[[level]] <- c(cl.by.hier[[level]], cl[i]);
   }
   return(cl.by.hier);
}

# Function to construct the TCDB annotation matrix
# Arguments:
# m : a data frame with the TCDB entries
# cl : a character vector with the names of the classes
# file: name of the text file in which the matrix will be written. If file="" (def.) no text file is written
# Value:
# The annotation matrix ann having proteins on rows and TCDB classe in columns.
# aa[i,j]=1 if protein i is annotated with class j, 0 otherwise.
do.ann.matrix <- function (m, cl,  file="") {
  
  prot.ac <- unique(as.character(m[,"AC"]));
  n.prot <- length(prot.ac);
  n.cl <- length(cl);
  ann <- matrix(integer(n.prot * n.cl), nrow=n.prot);
  rownames(ann) <- prot.ac;
  colnames(ann) <- cl;
  n.entry <- nrow(m);
  ac.entry <- as.character(m[,"AC"]);
  
  tc.ann <- as.character(m$TC);
  splitted.ann <- strsplit(tc.ann, "\\.");
  for (i in 1:n.entry) {
     z <- splitted.ann[[i]];
     y <- z[1];
     ann[ac.entry[i],y] <- 1;
     for (j in 2:5) {
        y <- paste0(y, ".", z[j]);
        ann[ac.entry[i],y] <- 1;
     }  
  }
  if (file !="")
    write.table(ann, file=file);
  return(ann);
}



# Function to construct the edge file of the TCDB graph 
# Arg:
# ann : character vector with the full TCDB annotations in the form  V.W.X.Y.Z
# filename : name of the file where edges will be stored
# Value:
# A file. Each row correspont to an edge of the form:
# parent_node    child_node
construct.tcdb.graph.egdes <- function(ann, filename="edges.txt") {
  SPACE = "    ";
  edges <- character();
  n <-length(ann);
  x <- strsplit(ann, "\\.");
  for (i in 1:n) {
     z <- x[[i]];
     y1 <- z[1];
     edges <- c(edges, paste("0", y1, sep=SPACE));
     for (j in 2:5) {
        y2 <- paste0(y1, ".", z[j]);
        edges <- c(edges, paste(y1, y2, sep=SPACE));
	y1 <- y2;
     }
  }
  edges <- sort(unique(edges));
  writeLines(edges, filename);
}



############### Auxiliary functions ###################################################

# Function to extract the first line for each protein of the TCDB
# The first line is the comment of the FASTA file and includes all the annotations of the TCDB
# Arguments:
# tcdb : name of the character vector having as rows the rows of the TCDB file
# Value:
# A character vector with the first line for each protein of the TCDB
extract.first.lines <- function(tcdb) {
  selected <- grep("^>gnl.*", tcdb); # extract only the first line of the FASTA entries
  # writeLines(tcdb[selected], "proteins.new.txt");
  tcdb.records <-  tcdb[selected];
  return(tcdb.records);
}



# Function to extract protein descriptions from the TCDB database
# Arguments:
# tcdb : name of the character vector having as rows the rows of the TCDB file
# filename: name of the file where the name of the proteins will be written: if "" (def.) no file is written.
# Value:
# A character vector with the names of the proteins
extract.protein.descr <- function(tcdb, filename="") {

  tcdb.records <- extract.first.lines(tcdb) # extract only the first line of the FASTA entries
  n.proteins <- length(tcdb.records)

  # extracting protein description for proteins having the OS= record
  indices.protein.with.OS <- grep(" .*OS=", tcdb.records);
  protein.names.pos <- regexpr(" .*OS=", tcdb.records);
  protein.names.OS.temp <- regmatches(tcdb.records, protein.names.pos);
  protein.names.OS <- gsub("^ {1}| OS=","",protein.names.OS.temp);
  
  # extracting protein descriptions for proteins not having the OS= record
  protein.names.without.OS.pos <- regexpr(" .*$", tcdb.records[-indices.protein.with.OS]);
  protein.names.without.OS.temp <- regmatches(tcdb.records[-indices.protein.with.OS], protein.names.without.OS.pos);
  protein.names.without.OS <- gsub("^ {1}","",protein.names.without.OS.temp);

  # putting together protein.names.OS and protein.names.without.OS
  protein.names <- character(n.proteins);
  protein.names[indices.protein.with.OS] <- protein.names.OS;
  protein.names[-indices.protein.with.OS] <- protein.names.without.OS;
  if (filename != "")
     writeLines(protein.names, filename);

  return(protein.names);
}

# Function to extract OS records from the TCDB database
# Arguments:
# tcdb : name of the character vector having as rows the rows of the TCDB file
# Value:
# A character vector with the OS of the proteins
extract.OS <- function(tcdb) {

  tcdb.records <- extract.first.lines(tcdb); # extract only the first line of the FASTA entries
  n.proteins <- length(tcdb.records);

  # extracting protein OS for proteins having the OS= record
  indices.protein.with <- grep("OS=", tcdb.records);
  protein.pos <- regexpr("OS=.*[GN=|PE=|SV=]", tcdb.records);
  protein.temp <- regmatches(tcdb.records, protein.pos);
  protein.with <- gsub("OS=| GN=.*| PE=.*| SV=.*","",protein.temp);

  # putting together protein.with and protein.without
  protein.feature <- character(n.proteins);
  protein.feature[indices.protein.with] <- protein.with;
  protein.feature[-indices.protein.with] <- "";


  return(protein.feature);
}

# Function to extract GN records from the TCDB database
# Arguments:
# tcdb : name of the character vector having as rows the rows of the TCDB file
# Value:
# A character vector with the GN of the proteins
extract.GN <- function(tcdb) {

  tcdb.records <- extract.first.lines(tcdb); # extract only the first line of the FASTA entries
  n.proteins <- length(tcdb.records);

  # extracting protein GN for proteins having the OS= record
  indices.protein.with <- grep("GN=", tcdb.records);
  protein.pos <- regexpr("GN=.*[PE=|SV=]", tcdb.records);
  protein.temp <- regmatches(tcdb.records, protein.pos);
  protein.with <- gsub("GN=| PE=.*| SV=.*","",protein.temp);

  # putting together protein.with and protein.without
  protein.feature <- character(n.proteins);
  protein.feature[indices.protein.with] <- protein.with;
  protein.feature[-indices.protein.with] <- "";


  return(protein.feature);
}

# Function to extract PE records from the TCDB database
# Arguments:
# tcdb : name of the character vector having as rows the rows of the TCDB file
# Value:
# A character vector with the PE of the proteins
extract.PE <- function(tcdb) {

  tcdb.records <- extract.first.lines(tcdb); # extract only the first line of the FASTA entries
  n.proteins <- length(tcdb.records);

  # extracting protein PE for proteins having the OS= record
  indices.protein.with <- grep("PE=", tcdb.records);
  protein.pos <- regexpr("PE=.*[SV=]", tcdb.records);
  protein.temp <- regmatches(tcdb.records, protein.pos);
  protein.with <- gsub("PE=| SV=.*","",protein.temp);

  # putting together protein.with and protein.without
  protein.feature <- character(n.proteins);
  protein.feature[indices.protein.with] <- protein.with;
  protein.feature[-indices.protein.with] <- "";


  return(protein.feature);
}


# Function to extract SV records from the TCDB database
# Arguments:
# tcdb : name of the character vector having as rows the rows of the TCDB file
# Value:
# A character vector with the SV of the proteins
extract.SV <- function(tcdb) {

  tcdb.records <- extract.first.lines(tcdb); # extract only the first line of the FASTA entries
  n.proteins <- length(tcdb.records);

  # extracting protein SV for proteins having the SV= record
  indices.protein.with <- grep("SV=", tcdb.records);
  protein.pos <- regexpr("SV=.*", tcdb.records);
  protein.temp <- regmatches(tcdb.records, protein.pos);
  protein.with <- gsub("SV=","",protein.temp);

  # putting together protein.with and protein.without
  protein.feature <- character(n.proteins);
  protein.feature[indices.protein.with] <- protein.with;
  protein.feature[-indices.protein.with] <- "";


  return(protein.feature);
}



# Function to extract the first multiple record from the TCDB database
# Note the first records has the format:
# >gnl|TC-DB|A0AAS1|1.C.52.1.24
# The subrecords are separated by the | character. In particular the third recod is the Swissprot AC number of the protein, while the fourth if the
# 5 digits TCDB classification code.
# Arguments:
# tcdb : name of the TCDB file
# Value:
# A character vector with the first multiple record
extract.first.record <- function(tcdb) {
  
  tcdb.records <- extract.first.lines(tcdb) # extract only the first line of the FASTA entries
  n.proteins <- length(tcdb.records);

  multiple.record <- strsplit(tcdb.records, " ");
  first.record <- character(n.proteins);
  for (i in 1:n.proteins)
    first.record[i] <- multiple.record[[i]][1];
  return(first.record);
}
     
# Function to extract Swissprot AC number from the TCDB database
# Note the first records has the format:
# >gnl|TC-DB|A0AAS1|1.C.52.1.24
# The subrecords are separated by the | character. In particular the third subrecod is the Swissprot AC number of the protein
# Arguments:
# tcdb : name of the character vector having as rows the rows of the TCDB file
# Value:
# A character vector with the Swissprot AC numbers
extract.SwissProt.AC <- function(tcdb) {
  
  first.record <- extract.first.record(tcdb);
  n.proteins <- length(first.record);

  multiple.record <- strsplit(first.record, "\\|");
  SwissProtAC.record <- character(n.proteins);
  for (i in 1:n.proteins)
    SwissProtAC.record[i] <- multiple.record[[i]][3];
  return(SwissProtAC.record);
}

# Function to extract the TCDB code from the TCDB database
# Note the first records has the format:
# >gnl|TC-DB|A0AAS1|1.C.52.1.24
# The subrecords are separated by the | character. In particular the fourth subrecord is the 5 digits TC code number of the protein
# Arguments:
# tcdb : name of the character vector having as rows the rows of the TCDB file
# Value:
# A character vector with the TCDB codes
extract.TCDB.code <- function(tcdb) {
  
  first.record <- extract.first.record(tcdb);
  n.proteins <- length(first.record);

  multiple.record <- strsplit(first.record, "\\|");
  TCDB.code.record <- character(n.proteins);
  for (i in 1:n.proteins)
    TCDB.code.record[i] <- multiple.record[[i]][4];
  return(TCDB.code.record);
}
 



# Function to find duplicates in a vector
# Arg:
# z : a vector
# Value:
# A vector with the duplicate entries. 
# Note: duplicates are repeated a numer of time equal to the number of duplications
find.duplicates <- function(z) {
  x <- as.character(m$AC);
  y <- sort(x);
  n <-length(y);
  dupl <- character(0);
  for (i in 1:(n-1)) {
    prev <- y[i];
    succ <- y[i+1];
    if (prev == succ)
      dupl <- c(dupl,prev);
  }
  return(dupl);
}





  

# Function to plot in compact way complex graphs
# Input:
# g: a graph
# node.label: a label plotted for each node
# fcolor : color of the node label
Plot.ontology.graph<-function(g, node.label="x", fcolor="black") {
  nAttrs<-list();
  z<-rep(node.label,length(nodes(g)));
  names(z)<-nodes(g);
  nAttrs$label<-z;
	attrs<-list(edge=list(color="grey"), node=list(fontcolor=fcolor));
  plot(g,nodeAttrs=nAttrs,attrs=attrs); 
}

# Function to "pretty" plot a graph 
# Input:
# g : a graph
# The other parameters corresponds to the global attributes of the node element of the list returned by getDefaultAttrs() of the graph package 
Pretty.plot.graph<-function(g,fontsize=12,fillcolor="lightgreen",height=0.6,width=0.9,color="black", fontcolor="black", lwd=1) {
 plot(g,"dot",attrs=list(node=list(fontsize=fontsize,height=height,fillcolor=fillcolor,width=width,shape="ellipse",fixedsize=FALSE,fontcolor=fontcolor, lwd=lwd)));
}

   
