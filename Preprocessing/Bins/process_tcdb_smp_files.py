


import re
for line in open('CDD/tcdb201509pssm.pn'):
    filename = line.strip()
    print filename
    fout = open('db/tcdb201509pssm/'+filename,'w')
    for line in open('CDD/'+filename):
        fout.write(re.sub('Query_1',re.sub('.smp','',filename),line))
    fout.close()
    

