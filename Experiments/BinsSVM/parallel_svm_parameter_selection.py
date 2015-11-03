




# The script uses Python thread and queue package.
# Implement worker class and queuing system.
# The framework looks at each parameter combination as a job and pools all job_queue in a queue.
# It generates a group of workers (computing nodes). 
# Each worker will always take and process the first job from the queue.
# In case that job is not completed by the worker, it will be push back to the queue, and will be processed later on.


import math             # enable math module for matrix etc.
import re               # enable regular expression
import Queue            
from threading import ThreadError
from threading import Thread
import os
import sys
import commands
sys.path.append('/cs/work/group/urenzyme/workspace/netscripts/')
from get_free_nodes import get_free_nodes
import multiprocessing
import time
import logging
import random
import itertools        # for list product
logging.basicConfig(format='%(asctime)s %(filename)s %(funcName)s %(levelname)s:%(message)s', level=logging.INFO)

job_queue = Queue.PriorityQueue()

# Worker class
# job is a tuple of parameters
class Worker(Thread):
  def __init__(self, job_queue, node):
    Thread.__init__(self)
    self.job_queue  = job_queue
    self.node = node
    self.penalty = 0 # penalty parameter which prevents computing node with low computational resources getting job_queue from job queue
    pass # def
  def run(self):
    all_done = 0
    while not all_done:
      try:
        time.sleep(random.randint(5000,6000) / 1000.0)  # get some rest :-)
        time.sleep(self.penalty*120) # bad worker will rest more
        job = self.job_queue.get(0)
        add_penalty = singleJob(self.node, job)
        self.penalty += add_penalty
        if self.penalty < 0:
          self.penalty = 0
      except Queue.Empty:
        all_done = 1
      pass # while
    pass # def
  pass # class


global_rundir = ''

# function to check if the result file already exist in the destination folder
def checkfile(filename):
  if os.path.exists(filename):
    if os.path.getsize(filename) > 0: return 1
    else: return 0
  else: return 0


def singleJob(node, job):
  (priority, job_detail) = job
  (paramInd,xFilename,yFilename,labelIndex,foldIndex,svmC,outputFilename,isTest) = job_detail
  try:
    if checkfile(outputFilename):
      logging.info('\t--< (priority) %d (node)%s (filename) %s' %(priority, node, outputFilename))
      fail_penalty = 0
    else:
      logging.info('\t--> (priority) %d (node)%s (filename) %s' %(priority, node, outputFilename))
      os.system(""" ssh -o StrictHostKeyChecking=no %s 'cd /cs/work/group/urenzyme/workspace/ProteinFunctionPrediction/Experiments/BinsSVM/; nohup matlab -nodisplay -nosplash -r "single_SVM '%s' '%s' '%s' '%s' '%s' '%s' '%s'" > /var/tmp/tmpsu'  """ % (node,xFilename,yFilename,labelIndex,foldIndex,svmC,outputFilename,isTest) )
      #print(""" ssh -o StrictHostKeyChecking=no %s 'cd /cs/work/group/urenzyme/workspace/ProteinFunctionPrediction/Experiments/BinsSVM/; nohup matlab -nodisplay -nosplash -r "single_SVM '%s' '%s' '%s' '%s' '%s' '%s' '%s'" > /var/tmp/tmpsu'  """ % (node,xFilename,yFilename,labelIndex,foldIndex,svmC,outputFilename,isTest) )
      logging.info('\t--| (priority) %d (node)%s (filename) %s' %(priority, node, outputFilename))
      fail_penalty = -1
      time.sleep(1)
  except Exception as excpt_msg:
    print excpt_msg
    job_queue.put((priority, job_detail))
    logging.info('\t--= (priority) %d (node)%s (filename) %s' %(priority, node, outputFilename))
    fail_penalty = 1
  if not checkfile(outputFilename):
    job_queue.put((priority,job_detail))
    logging.info('\t--x (priority) %d (node)%s (filename) %s' %(priority, node, outputFilename))
    fail_penalty = 1
  time.sleep(2)
  return fail_penalty
  pass

def run():
  logging.info('\t\tGenerating priority queue.')
  paramInd = 0
  kFold    = 5 
  numLabel = 3200  
  suffix   = 'sel'
  isTest   = '1'
  # iterate over the lists
  xFilenameList         = ['../Data/tcdb.TB',  '../Data/tcdb.TICoils',  '../Data/tcdb.TIGene3D',  '../Data/tcdb.TIHamap',  '../Data/tcdb.TIPANTHER',  '../Data/tcdb.TIPfam',  '../Data/tcdb.TIPhobius',  '../Data/tcdb.TIPIRSF',  '../Data/tcdb.TIPRINTS',  '../Data/tcdb.TIProDom',  '../Data/tcdb.TIProSitePatterns',  '../Data/tcdb.TIProSiteProfiles',  '../Data/tcdb.TISignalP_EUK',  '../Data/tcdb.TISignalP_GRAM_NEGATIVE',  '../Data/tcdb.TISignalP_GRAM_POSITIVE',  '../Data/tcdb.TISMART',  '../Data/tcdb.TISUPERFAMILY',  '../Data/tcdb.TITIGRFAM',  '../Data/tcdb.TITMHMM',  '../Data/tcdb.TPSI',  '../Data/tcdb.TRPSCDD',  '../Data/tcdb.TRPSCDDNCBI',  '../Data/tcdb.TRPSCOG',  '../Data/tcdb.TRPSKOG',  '../Data/tcdb.TRPSPFAM',  '../Data/tcdb.TRPSPRK',  '../Data/tcdb.TRPSSMART',  '../Data/tcdb.TRPSTCDB201509PSSM',  '../Data/tcdb.TRPSTIGR']
  xFilenameList = xFilenameList[25:]
  #xFilenameList         = ['../Data/tcdb.TB']
  yFilenameList         = ['../Data/tcdb.TC']
  labelIndexList        = xrange(1,numLabel+1)
  foldIndexList         = xrange(1,kFold+1) 
  cList    = ['0.01','0.1','1','10','100']
  # generate job queue, will iterate over c,k,label
  for xFilename,yFilename,labelIndex,foldIndex,svmC in list(itertools.product(xFilenameList,yFilenameList,labelIndexList,foldIndexList,cList)):
    tmpDir   = '../ResultsSVM/tmp_%s_%s/' % ( re.sub('.*/','',xFilename), re.sub('.*/','',yFilename))
    if not os.path.exists(tmpDir): os.mkdir(tmpDir)
    paramInd += 1
    outputFilename = tmpDir + '/' + re.sub('.*/','',xFilename) + '_' + re.sub('.*/','',yFilename) + '_l' + str(labelIndex) + '_f' + str(foldIndex) + '_c' +svmC + '_t' + isTest + '_' + suffix 
    ## check if result is ready already
    if checkfile(outputFilename): continue
    ## put parameter into queue
    job_queue.put( (paramInd,(str(paramInd),xFilename,yFilename,str(labelIndex),str(foldIndex),svmC,outputFilename,isTest)) )

  # get computing node
  logging.info('\t\tObtain cluster node')
  cluster = get_free_nodes()[0]
  #cluster = ['ukko133.hpc'] 

  # run jobs
  job_size = job_queue.qsize()
  logging.info( "\t\tProcessing %d job_queue" % (job_size))
  is_main_run_factor=1
  # running job_queue
  threads = []
  workerload = 3 
  for i in range(len(cluster)):
    for j in range(workerload):
      if job_queue.empty(): break
      t = Worker(job_queue, cluster[i])
      time.sleep(is_main_run_factor)
      try:
        t.start()
        threads.append(t)
      except ThreadError:
        logging.warning("\t\tError: thread error caught!")
    pass
  for t in threads:
    t.join()
    pass
  pass 


# it is not really necessary to have '__name__' space here, but what ever ...
if __name__ == "__main__":
  run()
  pass


