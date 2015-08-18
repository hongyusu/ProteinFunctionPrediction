

function compute_kernels()
  xFilenameList = {'../Data/tcdb.TC','../Data/tcdb.TB','../Data/tcdb.TICoils','../Data/tcdb.TIGene3D','../Data/tcdb.TIHamap','../Data/tcdb.TIPANTHER','../Data/tcdb.TIPfam','../Data/tcdb.TIPhobius','../Data/tcdb.TIPIRSF','../Data/tcdb.TIPRINTS','../Data/tcdb.TIProDom','../Data/tcdb.TIProSitePatterns','../Data/tcdb.TIProSiteProfiles','../Data/tcdb.TISignalP_EUK','../Data/tcdb.TISignalP_GRAM_NEGATIVE','../Data/tcdb.TISignalP_GRAM_POSITIVE','../Data/tcdb.TISMART','../Data/tcdb.TISUPERFAMILY','../Data/tcdb.TITIGRFAM','../Data/tcdb.TITMHMM'};

  if 1==0
  for i = 1:length(xFilenameList)
    xFilename = xFilenameList{i};
    m = dlmread(xFilename);
    m = m(2:size(m,1),2:size(m,2));
    if strcmp(xFilename,'../Data/tcdb.TC')
      mSum = sum(m,1);
      m = m(:,mSum>2);
    end
    K = m*m';
    K = centering(K);
    xFilename
    size(K)
    dlmwrite(sprintf('%s.K',xFilename),K);
  end
  end

  
  for i = 2:length(xFilenameList)
    i
    xFilename = xFilenameList{i};
    if i==2
      Kall = dlmread(sprintf('%s.K',xFilename));
    else
      Kall = Kall + dlmread(sprintf('%s.K',xFilename));
    end
  end
  Kall = Kall/size(xFilenameList,2);
  dlmwrite(sprintf('../Data/tcdb.all.K'),Kall);
end


function Kc=centering(K)

  ell = size(K,1);
  D = sum(K) / ell;
  E = sum(D) / ell;
  J = ones(ell,1) * D;
  Kc = K - J - J' + E * ones(ell, ell);
  
end
