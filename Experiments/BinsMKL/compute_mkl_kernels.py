

import sys
import numpy

def mkl(kFilenameList,yFilename,kType):

  '''
  kFilenameList:        list of input kernel file names
  yFilename:            output kernel file name
  kType:                multiple kernel learning method: uniform combination, align, alignf
  '''

  if kType == 'UNIMKL':
    for i,kFilename in enumerate(kFilenameList):
      print i,kFilename
      K = numpy.loadtxt(kFilename,delimiter=',')
      if i==0: Kall = numpy.zeros(K.shape)
      Kall = Kall + K/len(kFilenameList) 
    w = numpy.ones(len(kFilenameList))/len(kFilenameList)
    numpy.savetxt('../Data/tcdb.all.K%s'  % kType, Kall, fmt='%.2f', delimiter=',')
    numpy.savetxt('../Data/tcdb.all.KW%s' % kType, w,    fmt='%.2f', delimiter=',') 

  elif kType == 'ALIGN':
    Ky = numpy.loadtxt(yFilename,delimiter=',')
    w=[]
    for i,kFilename in enumerate(kFilenameList):
      print i,kFilename
      K = numpy.loadtxt(kFilename,delimiter=',')
      if i==0: Kall = numpy.zeros(K.shape)
      s = f_dot(K, Ky) / f_norm(K) / f_norm(Ky)
      w.append(s)
      Kall = Kall + s*K
    w = numpy.array(w)
    numpy.savetxt('../Data/tcdb.all.K%s'  % kType, Kall, fmt='%.2f', delimiter=',')
    numpy.savetxt('../Data/tcdb.all.KW%s' % kType, w,    fmt='%.2f', delimiter=',') 

  elif kType == 'ALIGNF':
    Ky = numpy.loadtxt(yFilename,delimiter=',')
    a = []
    for i,kFilename in enumerate(kFilenameList):
      print i,kFilename
      K = numpy.loadtxt(kFilename,delimiter=',')
      a.append(f_dot(K,Ky))
    a = numpy.array(a,dtype='d')
    M = numpy.zeros((len(kFilenameList), len(kFilenameList)),dtype='d')
    for i in range(len(kFilenameList)):
      Ki = numpy.loadtxt(kFilenameList[i],delimiter=',')
      for j in range(i,len(kFilenameList)):
        print i,j
        Kj = numpy.loadtxt(kFilenameList[j],delimiter=',')
        M[i,j] = f_dot(Ki, Kj)
        M[j,i] = M[i,j]
    try:
      from cvxopt import matrix
      from cvxopt import solvers
    except ImportError:
      raise ImportError("Module <cvxopt> needed for ALIGNF.")
    # define variable for cvxopt.qp
    P = matrix(2*M)
    q = matrix(-2*a)
    G = matrix(numpy.diag([-1.0]*len(kFilenameList)))
    h = matrix(numpy.zeros(len(kFilenameList),dtype='d'))
    sol = solvers.qp(P,q,G,h)
    w = sol['x']
    w = w/numpy.linalg.norm(w)
    # compute train_km with best w
    Kall = numpy.zeros(Ky.shape)
    for i in range(len(kFilenameList)):
      K = numpy.loadtxt(kFilenameList[i],delimiter=',')
      Kall = Kall + w[i]*K
    numpy.savetxt('../Data/tcdb.all.K%s'  % kType, Kall, fmt='%.2f', delimiter=',')
    numpy.savetxt('../Data/tcdb.all.KW%s' % kType, w,    fmt='%.2f', delimiter=',') 

    pass




def f_norm(k):
    """ Compute frobenius norm of the matrix k """
    return numpy.sqrt(numpy.trace(numpy.dot(k.T,k)))

def f_dot(k1,k2):
    """ Compute frobenius product of matrix k1, k2 """
    return numpy.trace(numpy.dot(k1.T,k2))







if __name__ == '__main__':

  kFilenameList = ['../Data/tcdb.TB.K',  '../Data/tcdb.TICoils.K',  '../Data/tcdb.TIGene3D.K',  '../Data/tcdb.TIHamap.K',  '../Data/tcdb.TIPANTHER.K',  '../Data/tcdb.TIPfam.K',  '../Data/tcdb.TIPhobius.K',  '../Data/tcdb.TIPIRSF.K',  '../Data/tcdb.TIPRINTS.K',  '../Data/tcdb.TIProDom.K',  '../Data/tcdb.TIProSitePatterns.K',  '../Data/tcdb.TIProSiteProfiles.K',  '../Data/tcdb.TISignalP_EUK.K',  '../Data/tcdb.TISignalP_GRAM_NEGATIVE.K',  '../Data/tcdb.TISignalP_GRAM_POSITIVE.K',  '../Data/tcdb.TISMART.K',  '../Data/tcdb.TISUPERFAMILY.K',  '../Data/tcdb.TITIGRFAM.K',  '../Data/tcdb.TITMHMM.K',  '../Data/tcdb.TPSI.K',  '../Data/tcdb.TRPSCDD.K',  '../Data/tcdb.TRPSCDDNCBI.K',  '../Data/tcdb.TRPSCOG.K',  '../Data/tcdb.TRPSKOG.K',  '../Data/tcdb.TRPSPFAM.K',  '../Data/tcdb.TRPSPRK.K',  '../Data/tcdb.TRPSSMART.K',  '../Data/tcdb.TRPSTCDB201509PSSM.K',  '../Data/tcdb.TRPSTIGR.K']

  yFilename = '../Data/tcdb.TC.K'

  #mkl(kFilenameList,yFilename,sys.argv[1])

  mkl(kFilenameList,yFilename,'ALIGN')
  mkl(kFilenameList,yFilename,'ALIGNF')
  mkl(kFilenameList,yFilename,'UNIMKL')



