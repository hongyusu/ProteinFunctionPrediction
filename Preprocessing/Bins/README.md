




# Directiary for preprocessing scripts

This directory consists of the following files used for data preprocessing

```
|---README.md                       # this file
|---process_tcdb.py                 # process tcdb database to remove duplication, and generate row labels and column labels
|---process_tcdb_smp_files.py       # This script is used to process the generated TCDB-CDD database in BLAST tool db folder
|---run_blast.sh                    # run BLAST serach on TCDB
|---run_interproscan.sh             # run interproscan on TCDB
|---run_rpsblast.py                 # run rpsblast on TCDB
|---run_psiblast.py                 # run psiblast on TCDB
|---merge_feature_files.py          # merge tcdb classification file, blast feature, and interproscan features
|---separate_features.py            # separate different feature into different matrices in ../Experiments/Data/ folder
|---compute_TC_edgelist.py          # Generate edge list of the TC hierarchical structure
|---Others                          # Other 'old' scripts
    |---get_intersection.py
    |---merge_datasets.py
```

# Other information

