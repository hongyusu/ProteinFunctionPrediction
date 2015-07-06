# Preliminary workplan
Please, add any modification/suggestion you wish.

## Preliminary experiments to evaluate the predictability of the TCDB classes

### Experiments using BLAST data and the about 12000 proteins having at least 1 annotation. 
We should exlude TCDB classes
having only 1 annotation, thus resulting in about 3414 classes (TCDB release 7 june 2015). As a consequence we may have also a reduced number of proteins (i.e. less than 12000).
Metrics: AUC per class  and precision at different level of recall. Evaluation: leave-one-out (loo). 
Results averaged across classes, across levels, and per class. 
    1. BLAST (best hit?) as (strong) baseline  (Su?)
    2. Nearest Neighbour 
    3. RANKS (Giorgio)		
    4. linear SVM? 	
		
### Selection of the InterPro features most informative for the prediction of transport proteins
### Definition of other non-InterPro features most meaningful for the prediction of transport proteins (e.g. TMS data)


## Design of Tree structured output methods for single-path predictions

## Design of hierarchical ensembles for single-path predictions

    Status API Training Shop Blog About Help 


