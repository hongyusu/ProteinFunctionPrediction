



%%
% compute the best svm C parameter for the input and output pair

function compute_best_svmC(xFilename,yFilename)

  Y = dlmread(sprintf(yFilename),' ');
  Y = Y(2:size(Y,1),2:size(Y,2));
  Ysum = sum(Y,1);
  Y = Y(:,Ysum>2);

  isTest = '1';
  suffix = 'sel';
  svmCList = {'0.01','0.1','1','10','100'};
  svmCList = {'0.01','0.1'};

  res = zeros(size(svmCList,1),2)
  for svmCIndex = 1:length(svmCList)
    svmC = svmCList{svmCIndex};
    res(svmCIndex,:) = compute_performance(xFilename,yFilename,svmC,isTest,suffix,Y);
  end
  res

end


%%
% 
% xFilename:            input feature
% yFilename:            output multiple label, label is either 0 or 1
% svmC:                 svm slack parameter
% isTest:               select a small port of data for sanity check if isTest=True  
%
function [auc,acc] = compute_performance(xFilename,yFilename,svmC,isTest,suffix,Y)

  Ypred = zeros(size(Y));

  for labelIndex = 1:30
    for foldIndex = 1:5
      % processing
      outputFilename = sprintf('../tmpDir/%s_%s_l%d_f%d_c%s_t%s_%s',...
      regexprep(xFilename,'.*/',''),...
      regexprep(yFilename,'.*/',''),...
      labelIndex,foldIndex,svmC,isTest,suffix);
      
      res = dlmread(outputFilename);
      Ypred(res(:,1),labelIndex) = res(:,2);
    end
  end

  accuracy = 1-sum(sum(xor(Y,Ypred)))/size(Y,1)/size(Y,2);
  [X,Y,T,auc] = perfcurve(reshape(Y,size(Y,1)*size(Y,2),1),reshape(Ypred,size(Y,1)*size(Y,2),1),1);
  
end
