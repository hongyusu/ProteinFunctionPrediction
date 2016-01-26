
import os
import re



def process_one_prefix(prefix):
  # collect protein id
  proteinidlist = []
  index = 0
  for line in open('../../Preprocessing/Results/tcdbdata.rowlab'):
    index += 1
    proteinidlist.append(index)
  # collect prefix id
  featureidlist = []
  index = 0
  for line in open('../../Preprocessing/Results/tcdbdata.collab'):
    index += 1
    if line.startswith(prefix):
      featureidlist.append(index)
  print len(proteinidlist),prefix,len(featureidlist),min(featureidlist),max(featureidlist)
  #
  data = {}
  for line in open('../../Preprocessing/Results/tcdbdata.mtx'):
    proteinid,featureid,score = line.strip().split(' ')
    proteinid = eval(proteinid)
    featureid = eval(featureid)
    score = eval(score)
    if not proteinid in data:
      data[proteinid] = {}
    if not featureid in featureidlist:
      continue
    else:
      if prefix[:4] in ['TB__','TPSI','TRPS']:
        if not featureid in data[proteinid]:
          data[proteinid][featureid] = score
        if data[proteinid][featureid] < score:
          data[proteinid][featureid] = score
      else:
          if not featureid in data[proteinid]:
            data[proteinid][featureid] = 0 
          data[proteinid][featureid] += 1
  # write
  fout = open('../../Experiments/Data/tcdb.%s' % re.sub('__','',prefix),'w')
  ## write header line
  fout.write('0 %s\n' % ' '.join(map(str,sorted(featureidlist))))
  ## write data
  for proteinid in sorted(proteinidlist):
      fout.write('%d' % proteinid)
      if not proteinid in data:
        fout.write('%s/n' % ' 0'*len(featureidlist))
      else:
        for featureid in sorted(featureidlist):
          if not featureid in data[proteinid]:
            fout.write(' 0')
          else:
            if prefix[:4] in ['TB__','TPSI','TRPS']:
              fout.write(' %.2f' % data[proteinid][featureid])
            else:
              fout.write(' %d' % data[proteinid][featureid])
      fout.write('\n')
  fout.close()
     
  pass
    


def separate_features():
  prefixlist = ['TB__','TC__','TICoils__','TIGene3D__','TIHamap__','TIPANTHER__','TIPfam__','TIPhobius__','TIPIRSF__','TIPRINTS__','TIProDom__','TIProSitePatterns__','TIProSiteProfiles__','TISignalP_EUK__','TISignalP_GRAM_NEGATIVE__','TISignalP_GRAM_POSITIVE__','TISMART__','TISUPERFAMILY__','TITIGRFAM__','TITMHMM__','TPSI__','TRPSCDD__','TRPSCDDNCBI__','TRPSCOG__','TRPSKOG__','TRPSPFAM__','TRPSPRK__','TRPSSMART__','TRPSTCDB201509PSSM__','TRPSTIGR__']
  for prefix in prefixlist:
      process_one_prefix(prefix)
  pass

def copy_names():
  os.system('cp ../../Preprocessing/Results/tcdbdata.collab ../../Experiments/Data/tcdb.collab')
  os.system('cp ../../Preprocessing/Results/tcdbdata.rowlab ../../Experiments/Data/tcdb.rowlab')
  pass

if __name__ == '__main__':
  separate_features()
  copy_names()





