



%%=========
% 
% xFilename:            input feature
% yFilename:            output multiple label, label is either 0 or 1
% EFilename:            edgelist
% foldIndex:            index of the fold in 5-fold cv
% sopC:                 margin slack parameter
% outputFilename:       tmp directory for results
% isTest:               select a small port of data for sanity check if isTest=True  
%%========

function single_SOP(xFilename,yFilename,EFilename,SFilename,foldIndex,sopC,outputFilename,logFilename,isTest)

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
  K = dlmread(xFilename,','); %Kd = diag(K);Kd(Kd==0) = 1;K = K ./ ( sqrt(Kd) * sqrt(Kd)' );
  S = dlmread(SFilename,' ');
  Y = dlmread(yFilename,' ');
  Y = Y(2:size(Y,1),2:size(Y,2));
  
  % restrict the search space to all the labels seen in training and test sets
  S = unique(Y,'rows');
  
  
  % some global parameter
  smallN = 500;
  smallN = min(smallN,size(K,1));

  % selection: selecting labels with more than two proteins
  % do not perform selection, as the output graph is build for all labels indexed from 1
  %Ysum = sum(Y,1);
  %Y = Y(:,Ysum>2);

  % sample a small subset for test
  if isTest
    K = K(1:smallN,1:smallN);
    Y = Y(1:smallN,:);
  end

  % cross validation index, 5 fold
  Ind = crossvalind('Kfold',size(K,1),5);

  % separate training and test data
  Ktr = K(Ind~=foldIndex,Ind~=foldIndex);
  Ytr = Y(Ind~=foldIndex,:); Ytr(Ytr==0)=-1;
  Kts = K(Ind==foldIndex,Ind~=foldIndex);
  Yts = Y(Ind==foldIndex,:); Yts(Yts==0)=-1;
  S(S==0) = -1;
  
  % set parameter
  paramsIn.profileiter    = 1;            % Profile the training every fix number of iterations
  paramsIn.maxiter        = 30;           % maximum number of iterations in the outer loop
  paramsIn.mlloss         = 0;            % assign loss to microlabels(0) edges(1)
  paramsIn.epsilon        = 1E-6;         % stopping criterion: minimum relative duality gap
  paramsIn.C              = sopC;         % margin slack
  paramsIn.tolerance      = 1E-10;        % numbers smaller than this are treated as zero
  paramsIn.verbosity      = 1;
  paramsIn.logFilename    = logFilename;            % log file name
  paramsIn.outputFilename = outputFilename;         % output filename
  paramsIn.foldIndex      = foldIndex;              % fold index
  paramsIn.exampleIndex   = find(Ind==foldIndex);   % index of examples

  % set input data
  dataIn.S   = S;          % search space
  dataIn.E   = E;          % edge
  dataIn.Ktr =  Ktr;       % training kernel
  dataIn.Kts =  Kts';      % test kernel
  dataIn.Ytr =  Ytr;       % training label
  dataIn.Yts =  Yts;       % test label
    
  % training and prediction
  TCSOP (paramsIn, dataIn);
    
    
    
end

