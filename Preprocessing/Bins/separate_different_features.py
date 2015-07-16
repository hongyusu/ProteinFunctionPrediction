

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
      if prefix in ['TB__']:
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
            if prefix in ['TB__']:
              fout.write(' %.2f' % data[proteinid][featureid])
            else:
              fout.write(' %d' % data[proteinid][featureid])
      fout.write('\n')
  fout.close()
     
  pass
    


def separate_features():
  prefixlist = ['TC__', 'TB__', 'TIProDom__', 'TIHamap__', 'TISMART__', 'TISUPERFAMILY__', 'TIPRINTS__', 'TIPANTHER__', 'TIGene3D__', 'TIPIRSF__', 'TIPfam__', 'TIProSiteProfiles__', 'TITIGRFAM__', 'TIProSitePatterns__', 'TICoils__', 'TITMHMM__', 'TIPhobius__', 'TISignalP_GRAM_NEGATIVE__', 'TISignalP_EUK__', 'TISignalP_GRAM_POSITIVE__']
  for prefix in prefixlist:
      process_one_prefix(prefix)
  pass

if __name__ == '__main__':
  separate_features()
