




%%
% 
% xFilename:            input feature
% yFilename:            output multiple label, label is either 0 or 1
% labelIndex:           index of a single label in multilabel
% foldIndex:            index of the fold in 5-fold cv
% svmC:                 svm slack parameter
% outputFilename:       tmp directory for results
% isTest:               select a small port of data for sanity check if isTest=True  
%
function single_SVM(xFilename,yFilename,labelIndex,foldIndex,svmC,outputFilename,isTest)

  % some global parameter
  smallN = 5000;

  % random number generator
  rand('twister',0)

  % process input argument 
  labelIndex = eval(labelIndex);
  foldIndex  = eval(foldIndex);
  svmC       = eval(svmC);
  isTest     = eval(isTest);

  % add svm matlab path
  addpath '~/softwares/libsvm-3.12/matlab/'

  % read in input and output files
  X = dlmread(xFilename,' ');
  X = X(2:size(X,1),2:size(X,2));
  Y = dlmread(yFilename,' ');
  Y = Y(2:size(Y,1),2:size(Y,2));

  % selection: selecting labels with more than two proteins
  Ysum = sum(Y,1);
  Y = Y(:,Ysum>2);

  if labelIndex > size(Y,2)
    res = [0,0];
    dlmwrite(outputFilename, res); 
    exit
  end

  % sample a small subset for test
  if isTest
    X = X(1:smallN,:);
    Y = Y(1:smallN,:);
  end

  % normalization: centering
  X = X - repmat(mean(X),size(X,1),1);
  X = X ./ repmat(std(X),size(X,1),1);
  
  % cross validation index, 5 fold
  Ind = crossvalind('Kfold',size(X,1),5);

  % separate training and test data
  Xtr = X(Ind~=foldIndex,:);
  Ytr = Y(Ind~=foldIndex,labelIndex);
  Xts = X(Ind==foldIndex,:);
  Yts = Y(Ind==foldIndex,labelIndex);

  if length(unique(Ytr))==1
    YtrUnique = unique(Ytr);
    Yprobsvm = Yts*1+YtrUnique(1)
  else
    % training
    model = svmtrain(Ytr,Xtr,sprintf('-q -s 0 -c %.2f -t 1 -b 1',svmC));
    % prediction
    [~,~,Yprobsvm] = svmpredict(Yts,Xts, model ,'-b 1');
    Yprobsvm = clear_prob(Ytr,Yprobsvm);
  end
  % save the results
  res = [find(Ind==foldIndex),Yprobsvm];
  dlmwrite(outputFilename, res); 

  exit;

end

function Yprobsvm = clear_prob(Ytr,Yprobsvm)
    if Ytr(1) == 0
        Yprobsvm = Yprobsvm(:,2);
    end
    if Ytr(1) == 1
        Yprobsvm = Yprobsvm(:,1);
    end
end



