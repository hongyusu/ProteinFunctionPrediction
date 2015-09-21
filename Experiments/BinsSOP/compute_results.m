


function compute_results()
  xFilenameList         = {'tcdb.all.GUNIMKL','tcdb.all.GALIGN','tcdb.all.GALIGNF'};
  foldIndexList         = {'1','2','3','4','5'}; 
  cList                 = {'1000','5000','10000','50000'};
  stepSize1List         = {'7','9','11'};
  stepSize2List         = {'7','9','11'};


  pfileID = fopen('./parameters','a');
  for fileI=1:length(xFilenameList)

    resfilename = sprintf('../ResultsSOP/%s_tcdb.TC', xFilenameList{fileI}); 

    if exist(resfilename,'file') ~= 2
      Yp = [];
      for foldI=1:length(foldIndexList)

        results = [];
        filenames = cell(1,1000);
        index = 0;
        for cI=1:length(cList)
          for stepSize1I=1:length(stepSize1List)
            for stepSize2I=1:length(stepSize2List)
              filename =sprintf('../ResultsSOP/tmp_%s_tcdb.TC/%s_tcdb.TC_f%s_c%s_s1%s_s2%s_t0_sel.mat',xFilenameList{fileI},xFilenameList{fileI},foldIndexList{foldI},cList{cI},stepSize1List{stepSize1I},stepSize2List{stepSize2I});
              if exist(filename, 'file') == 2
                load(filename);
                index = index+1;
                results = [results;test_err];
                filenames{index} = filename;
              end
            end
          end
        end
        [X,I] = sortrows(results,[1,2]);
        filename = filenames{I(1)};  
        fprintf(pfileID,'%s\n',filename);
        load(filename);
        test_err
        Yp = [Yp;Yts];

      end
  
      Yp = sortrows(Yp,[1]);
      Yp = Yp(:,2:size(Yp,2));
      dlmwrite(resfilename,Yp);

    else
      Yp = dlmread(resfilename);
    end

    Yp(Yp==-1)=0;

    Y = dlmread('../Data/tcdb.TC',' ');
    Y = Y(2:size(Y,1),2:size(Y,2));
  
    mlaccuracy = sum(sum(Yp~=Y,2) == 0)/size(Y,1);

    tp = sum(sum((Y+Yp)==2));
    tn = sum(sum((Y+Yp)==0));
    fp = sum(sum((Y-Yp)==-1));
    fn = sum(sum((Y-Yp)==1));
    
    recall    = tp / (tp + fn);
    precision = tp / (tp + fp); 
    f1 = 2*precision*recall / (precision+recall);
    accuracy = 1-sum(sum(xor(Y,Yp)))/size(Y,1)/size(Y,2);
    res = [nan,nan,accuracy,f1,precision,recall,mlaccuracy]

    fileID = fopen('../ResultsSOP/results','a');
    fprintf(fileID, '%s %.4f %.4f %.4f %.4f %.4f %.4f %.4f\n',xFilenameList{fileI},res(1),res(2),res(3),res(4),res(5),res(6),res(7));
    fclose(fileID);
    
  end
  fclose(pfileID);

end
