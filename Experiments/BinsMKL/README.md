


# Bins for MKL

1. This folder contains the following files:
   ```
   |---README.md                                   # this file
   |---compute_base_kernels.m                      # compute base kernels
   |---compute_mkl_kernels.py                      # Compute UNIMKL, ALIGN, ALIGNF kernels
   |---single_kernelSVM.m                          # SVM learner on one single label, one fold, one SVM C parameter setting
   |---parallel_kernelsvm_parameter_selection.py   # run svm in parallel for parameter selection
   |---compute_best_kernelsvmC.m                   # compute the best parameter from parameter selection
   |---parameter_setting                           # parameter setting for different data
   |---parallel_kernelsvm.py                       # run svm in parallem for training and testing (cross validation)
   |---compute_results.m                           # compute auc and acc for the experiment
   |---plot_auc_curve.m                            # plot AUC curve
   |---cvxopt-1.1.7/                               # convex optimization toolbox
   |---savefigure/                                 # save matlab plot toolbox
   ```



