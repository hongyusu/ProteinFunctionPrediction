



%%=========
% 
% xFilename:            input feature
% yFilename:            output multiple label, label is either 0 or 1
% labelIndex:           index of a single label in multilabel
% foldIndex:            index of the fold in 5-fold cv
% svmC:                 svm slack parameter
% outputFilename:       tmp directory for results
% isTest:               select a small port of data for sanity check if isTest=True  
%%========

function single_SOP(xFilename,yFilename,EFilename,foldIndex,sopC,outputFilename,isTest)

  % some global parameter
  smallN = 5000;

  % random number generator
  rand('twister',0)

  % process input argument 
  foldIndex  = eval(foldIndex);
  sopC       = eval(sopC);
  isTest     = eval(isTest);

  % add svm matlab path
  addpath '~/softwares/libsvm-3.12/matlab/'

  % read in input and output files
  E = dlmread(EFilename,',');
  K = dlmread(xFilename,',');
  Y = dlmread(yFilename,' ');
  Y = Y(2:size(Y,1),2:size(Y,2));

  % selection: selecting labels with more than two proteins
  Ysum = sum(Y,1);
  Y = Y(:,Ysum>2);

  % sample a small subset for test
  if isTest
    K = K(1:smallN,1:smallN);
    Y = Y(1:smallN,:);
  end

  % cross validation index, 5 fold
  Ind = crossvalind('Kfold',size(K,1),5);

  % separate training and test data
  Ktr = K(Ind~=foldIndex,Ind~=foldIndex);
  Ytr = Y(Ind~=foldIndex,labelIndex); Ytr(Ytr==0)=-1;
  Kts = K(Ind==foldIndex,Ind~=foldIndex);
  Yts = Y(Ind==foldIndex,labelIndex); Yts(Yts==0)=-1;

  % set parameter
  paramsIn.profileiter    = profile_iteration;  % Profile the training every fix number of iterations
  paramsIn.losstype       = losstype;     % losstype
  paramsIn.mlloss         = 0;            % assign loss to microlabels(0) edges(1)
  paramsIn.profiling      = 1;            % profile (test during learning)
  paramsIn.epsilon        = sop_g;        % stopping criterion: minimum relative duality gap
  paramsIn.C              = sopC;         % margin slack
  paramsIn.max_CGD_iter   = 1;            % maximum number of conditional gradient iterations per example
  paramsIn.max_LBP_iter   = 3;            % number of Loopy belief propagation iterations
  paramsIn.tolerance      = 1E-10;        % numbers smaller than this are treated as zero
  paramsIn.maxiter        = mmcrf_i;      % maximum number of iterations in the outer loop
  paramsIn.verbosity      = 1;
  paramsIn.debugging      = 3;
  paramsIn.filestem       = sprintf('%s',suffix);	% file name stem used for writing output
  paramsIn.loss_scaling_factor = loss_scaling_factor;
  paramsIn.newton_method  = newton_method;
  paramsIn.tmpdir        = tmpdir;

  % set input data
  dataIn.Elist =  Elist;      % edge
  dataIn.Kx_tr =  Ktr;        % training kernel
  dataIn.Kx_ts =  Kts';       % test kernel
  dataIn.Y_tr  =   Ytr;       % training label
  dataIn.Y_ts  =   Yts;       % test label
    
    % running
    [rtn,~] = RSTA (paramsIn, dataIn);
    % save margin dual mu
    muList{k} = rtn;
    % collecting results
    load(sprintf('%s/Ypred_%s.mat', tmpdir, paramsIn.filestem));
    Ypred(Itest,:) = Ypred_ts;          % The prediction in binary value
    %YpredVal(Itest,:) = Ypred_ts_val;  % The prediction in real value
    running_times(k,1) = running_time;  % Running time of the algorithm on the Kth fold
    
    
    
    
end

