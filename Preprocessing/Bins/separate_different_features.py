

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
  print len(proteinidlist),prefix,len(featureidlist)
  #
  data = {}
  for line in open('../../Preprocessing/Results/tcdbdata.mtx'):
    proteinid,featureid,score = line.strip().split(' ')
    proteinid = eval(proteinid)
    featureid = eval(featureid)
    if not proteinid in data:
      data[proteinid] = {}
    if featureid in featureidlist:
      data[proteinid][featureid] = score
  # write
  fout = open('../../Experiments/Data/tcdb.%s' % re.sub('__','',prefix),'w')
  fout.write('0 %s\n' % ' '.join(map(str,sorted(featureidlist))))
  for proteinid in sorted(proteinidlist):
      fout.write('%d' % proteinid)
      if not proteinid in data:
        fout.write('%s/n' % ' 0'*len(featureidlist))
      else:
        for featureid in sorted(featureidlist):
          if not featureid in data[proteinid]:
            fout.write(' 0')
          else:
            fout.write(' %s' % data[proteinid][featureid])
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
