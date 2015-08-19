
function compute_results()

  [xFilenameList,yFilenameList,svmCList] = textread('parameter_setting','%s %s %s');
  for i=1:size(xFilenameList,1)
    tStart = tic;
    compute_results_single_dataset(xFilenameList{i},yFilenameList{i},svmCList{i});
    tEnd = toc(tStart)
  end

end




function compute_results_single_dataset(xFilename,yFilename,svmC)

  Y = dlmread(yFilename,' ');
  Y = Y(2:size(Y,1),2:size(Y,2));
  Ysum = sum(Y,1);
  Y = Y(:,Ysum>2);

  isTest = '0';
  suffix = 'val';
  res = zeros(1,5);
  [auc,accuracy,f1,precision,recall] = compute_performance(xFilename,yFilename,svmC,isTest,suffix,Y);
  res = [auc,accuracy,f1,precision,recall];
  res

  
  fileID = fopen('../ResultsMKL/results','a');
  fprintf(fileID, '%s %s %.4f %.4f %.4f %.4f %.4f\n',xFilename,yFilename,res(1),res(2),res(3),res(4),res(5));
  fclose(fileID);

end


%%
% 
% xFilename:            input feature
% yFilename:            output multiple label, label is either 0 or 1
% svmC:                 svm slack parameter
% isTest:               select a small port of data for sanity check if isTest=True  
%
function [auc,accuracy,f1,precision,recall] = compute_performance(xFilename,yFilename,svmC,isTest,suffix,Y)

  allOutputFilename = sprintf('../ResultsMKL/%s_%s_c%s_t%s_%s',...
      regexprep(xFilename,'.*/',''),...
      regexprep(yFilename,'.*/',''),...
      svmC,isTest,suffix);
  if exist(allOutputFilename) == 2
    Ypred = dlmread(allOutputFilename);
  else
    Ypred = zeros(size(Y));
  
    for labelIndex = 1:size(Y,2)
      for foldIndex = 1:5
        % processing
        outputFilename = sprintf('../ResultsMKL/%s_%s/%s_%s_l%d_f%d_c%s_t%s_%s',...
        regexprep(xFilename,'.*/',''),...
        regexprep(yFilename,'.*/',''),...
        regexprep(xFilename,'.*/',''),...
        regexprep(yFilename,'.*/',''),...
        labelIndex,foldIndex,svmC,isTest,suffix);
        
        res = dlmread(outputFilename);
        Ypred(res(:,1),labelIndex) = res(:,2);
      end
    end
    dlmwrite(allOutputFilename,Ypred);
  end
 


  [Xs,Ys,T,auc] = perfcurve(reshape(Y,size(Y,1)*size(Y,2),1),reshape(Ypred,size(Y,1)*size(Y,2),1),1);

  dlmwrite(sprintf('../ResultsMKL/perf_%s_%s',regexprep(xFilename,'.*/',''),regexprep(yFilename,'.*/','')),[Xs,Ys]);

  Ypred = Ypred>0.5;
  tp = sum(sum((Y+Ypred)==2));
  tn = sum(sum((Y+Ypred)==0));
  fp = sum(sum((Y-Ypred)==-1));
  fn = sum(sum((Y-Ypred)==1));

  recall    = tp / (tp + fn);
  precision = tp / (tp + fp); 
  f1 = 2*precision*recall / (precision+recall);
  accuracy = 1-sum(sum(xor(Y,Ypred)))/size(Y,1)/size(Y,2);

  
  
end
