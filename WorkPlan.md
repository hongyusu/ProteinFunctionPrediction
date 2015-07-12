# Preliminary workplan
Please, add any modification/suggestion you wish.

## Preliminary experiments to evaluate the predictability of the TCDB classes

### Experiments using BLAST data and the proteins more than 1 annotation. 
We should exlude TCDB classes having only 1 annotation, thus resulting in about 2436 classes (according to tcdb.1). 
The gzipped text file tcdb1.annotations.levels1234.MoreThan1.txt.gz in the directory Experiments/Data is a matrix with 12546 proteins (rows) and  2436 TC classes (columns): only classes with more than 1 annotation are included. In this way, in principle, using leave-one-out we could try to predict all the classes.

- At first we could use BLAST data just prepared by Su to understand whether we can predict something.

- As a second step we could try to add Interpro features.

- Metrics: AUC per class  and precision at different level of recall. Evaluation: leave-one-out (loo). 
Results averaged across classes, across levels, and per class.

- Preliminary flat methods that could be considered:

    1. BLAST (best hit?) as (strong) baseline  
    2. Nearest Neighbour 
    3. Semi-supervised flat learning methods: GBA and RANKS (Giorgio)		
    4. linear SVM and/or logistic regression or some other linear method. 	

Su could you perform task 1, 2 and 4? (of course if you agree on this set-up ...)
	
### Experiments using InterPro features
TO DO
### Definition of other non-InterPro features most meaningful for the prediction of transport proteins (e.g. TMS data)
TO DO

## Design of Tree structured output methods for single-path predictions
TO DO

## Design of hierarchical ensembles for single-path predictions
TO DO

    Status API Training Shop Blog About Help 


