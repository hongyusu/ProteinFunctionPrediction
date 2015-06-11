



def get_intersection():
  s = ''
  ptname = ''
  features = [0,0,0,0,0]
  for line in open('../../Preprocessing/Results/data'):
    words = line.strip().split(' ')
    if ptname == '':
      ptname = words[0]
    if not ptname == words[0]:
      # process
      s += '%s %s\n' % (words[0],' '.join(map(str,features)))
      # initialize
      ptname == words[0]
      features = [0,0,0,0,0]
    if words[1].startswith('G'):
      features[0] += 1
    if words[1].startswith('B'):
      features[1] += 1
    if words[1].startswith('P'):
      features[2] += 1
    if words[1].startswith('T') and not words[1].startswith('TC'):
      features[3] += 1
    if words[1].startswith('TC'):
      features[4] += 1
  s += '%s %s\n' % (words[0],' '.join(map(str,features)))
  fout = open('../../Preprocessing/Results/data_statistics','w')
  fout.write(s)
  fout.close()


if __name__ == '__main__':
  get_intersection()
