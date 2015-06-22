# script to process TCDB files in text format

source("TCDB.R");
source("IOgraph.R");

# 1. reading and parsing the tcdb text file and extracting the annotations.
m <- do.TCDB("tcdb.new.txt", file="tcdb.ann.7june2015.txt");

save(m, file="tcdb7june2015.rda");

# 2. construction of the annotation tables
cl <- extract.classes(m$TC); # 12587 classes

cl.by.level <- do.class.by.level (cl);

# the overall annotation table including al the 5 levels
ann <- do.ann.matrix (m,cl, file="ann.txt");
save(ann, file="ann.rda");

# annotations limited to each level
ann1 <- ann[, cl.by.level[[1]] ];
save(ann1, file="ann1.rda");
ann2 <- ann[, cl.by.level[[2]]];
save(ann2, file="ann2.rda");
ann3 <- ann[, cl.by.level[[3]]];
save(ann3, file="ann3.rda");
ann4 <- ann[, cl.by.level[[4]]];
save(ann4, file="ann4.rda");
ann5 <- ann[, cl.by.level[[5]]];
save(ann5, file="ann5.rda");

rm(ann);
gc();
# annotations up to a given level
ann12 <- cbind(ann1,ann2);
write.table(ann12, file="ann12.txt");
ann123 <- cbind(ann12, ann3);
write.table(ann123, file="ann123.txt");
ann1234 <- cbind(ann123, ann4);
write.table(ann1234, file="ann1234.txt");
rm(ann1,ann2,ann3,ann4,ann12,ann123,ann1234);
gc();

# 3. Construction of the tree representing the TCDB taxonomy
tcdb <- readLines("tcdb.new.txt");
TCDB.code <- extract.TCDB.code (tcdb);

# the ovrall tree including all the five levels in a "per-edge" file format
edges <- construct.tcdb.graph.egdes(TCDB.code);

# the overal tree represented as an R graphNEL class
g <- read.graph(file="edges.txt");
save (g, file="tcdb.tree.rda");
# the TCDB tree limited to the first 2, 3 and 4 levels:
g2 <- subGraph(c(cl.by.level[[1]], cl.by.level[[2]]), g);
save (g2, file="tcdb2levels.tree.rda");
g3 <- subGraph(c(cl.by.level[[1]], cl.by.level[[2]], cl.by.level[[3]]), g);
save (g3, file="tcdb3levels.tree.rda");
g4 <- subGraph(c(cl.by.level[[1]], cl.by.level[[2]], cl.by.level[[3]], cl.by.level[[4]]), g);
save (g4, file="tcdb4levels.tree.rda");

# plotting the two-levels tree
# plot(g2);
