

## Data matrices of different types

1. These files are not uploaded into Github individually due to the size limit of 100MB.

1. However, they are uploaded as a compressed tar packages.

1. Feature maps:
   1. First row (header line), '0 feature_id1 feature_id2 feature_id3 ...'
   2. Other rows (data), 'protein_id feature_id1_val feature_id2_val ...'
   1. File `./tcdb.TC` corresponds to multiple labels of proteins. Features (labels) are generated from a hierarchical structure of transporter protein classification system (TCDB) where both leave nodes and internal nodes are included. 

1. Kernels:
   1. *.K, linear kernel computed from the corresponding feature map, centered
   1. *.k, linear kernel computed from the corresponding feature map, normalized then centered





