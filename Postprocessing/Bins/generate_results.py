




def generate_results(inputFilename):
  results = {}
  for i,line in enumerate(open('../../Experiments/Data/tcdb.TC')):
    if i == 0:
      pos2id = line.strip().split(' ') 
    else:
      words = line.strip().split(' ')
      results[words[0]] = []
      for key,val in enumerate(words):
        if key == 0: continue 
        if not val == '0': results[words[0]].append( key )

  #for i,line in enumerate(open('../../Experiments/ResultsSOP/tcdb.all.KUNIMKL_tcdb.TC')):
  if inputFilename.startswith('../../Experiments/ResultsSOP'):
    for i,line in enumerate(open(inputFilename)):
      for key,val in enumerate(line.strip().split(',')):
        if not val == '-1': results[str(i+1)].append( key+1 )
  if inputFilename.startswith('../../Experiments/ResultsMKL'):
    for i,line in enumerate(open(inputFilename)):
      for key,val in enumerate(line.strip().split(',')):
        if not eval(val) >= 0.5: results[str(i+1)].append( key+1 )

  statistics = [0,0,0,0]
  n = 0
  fout = open('../Results/results','a')
  for key in results.keys():
    print results[key]
    n+=1
    if results[key][0] == results[key][4]: statistics[0]+=1
    if results[key][1] == results[key][5]: statistics[1]+=1
    if results[key][2] == results[key][6]: statistics[2]+=1
    if results[key][3] == results[key][7]: statistics[3]+=1
  fout.write ( "%s %.4f %.4f %.4f %.4f\n" % (inputFilename,statistics[0]/float(n),statistics[1]/float(n),statistics[2]/float(n),statistics[3]/float(n)))
  fout.close()
  pass

if __name__ == '__main__':
  #generate_results('../../Experiments/ResultsSOP/tcdb.all.KUNIMKL_tcdb.TC')
  #generate_results('../../Experiments/ResultsSOP/tcdb.all.KALIGN_tcdb.TC')
  #generate_results('../../Experiments/ResultsSOP/tcdb.all.KALIGNF_tcdb.TC')
  #generate_results('../../Experiments/ResultsSOP/tcdb.all.GUNIMKL_tcdb.TC')
  #generate_results('../../Experiments/ResultsSOP/tcdb.all.GALIGN_tcdb.TC')
  #generate_results('../../Experiments/ResultsSOP/tcdb.all.GALIGNF_tcdb.TC')

  generate_results('../../Experiments/ResultsMKL/tcdb.all.GALIGNF_tcdb.TC_c1_t0_val')
  generate_results('../../Experiments/ResultsMKL/tcdb.all.GALIGN_tcdb.TC_c1_t0_val')
  generate_results('../../Experiments/ResultsMKL/tcdb.all.GUNIMKL_tcdb.TC_c0.1_t0_val')
  generate_results('../../Experiments/ResultsMKL/tcdb.all.KALIGNF_tcdb.TC_c10_t0_val')
  generate_results('../../Experiments/ResultsMKL/tcdb.all.KALIGN_tcdb.TC_c0.1_t0_val')
  generate_results('../../Experiments/ResultsMKL/tcdb.all.KUNIMKL_tcdb.TC_c1_t0_val')






  
 
 

