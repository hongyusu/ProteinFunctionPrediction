



# ======================================================
# The script uses Python thread and queue package.
# Implement worker class and queuing system.
# The framework looks at each parameter combination as a job and pools all job_queue in a queue.
# It generates a group of workers (computing nodes). 
# Each worker will always take and process the first job from the queue.
# In case that job is not completed by the worker, it will be push back to the queue, and will be processed later on.
# ======================================================


__author__ = 'Hongyu Su'
__email__ = 'hongyu.su@me.com'
__version__ = '1.0'

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
  '''
  worker class implemented with Python thread and queue class to enable each worker (a computing node) executes jobs independently
  '''
  def __init__(self, job_queue, node):
    '''initialization function for workers'''
    Thread.__init__(self)
    self.job_queue  = job_queue
    self.node = node
    self.penalty = 0 # penalty parameter which prevents computing node with low computational resources getting job_queue from job queue
    pass # def
  def run(self):
    '''take job from job queue and execute the job'''
    all_done = 0
    while not all_done:
      try:
        time.sleep(random.randint(20000,30000) / 100.0)  # get some rest :-)
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
  ''' function to check if the file already exist '''
  if os.path.exists(filename):
    if os.path.getsize(filename) > 0: return 1
    else: return 0
  else: return 0


def singleJob(node, job):
  '''
  single computing job that will be deployed on a computing node of the cluster
  '''
  (priority, job_detail) = job
  (paramInd,xFilename,yFilename,EFilename,SFilename,foldIndex,sopC,outputFilename,logFilename,stepSize1,stepSize2,isTest,suffix) = job_detail
  try:
    if checkfile(outputFilename):
      logging.info('\t--< (priority) %d (node)%s (filename) %s' %(priority, node, outputFilename))
      fail_penalty = 0
    else:
      logging.info('\t--> (priority) %d (node)%s (filename) %s' %(priority, node, outputFilename))
      os.system(""" ssh -o StrictHostKeyChecking=no %s 'cd /cs/work/group/urenzyme/workspace/ProteinFunctionPrediction/Experiments/BinsSOP/; nohup matlab -nodisplay -nosplash -r "single_SOP '%s' '%s' '%s' '%s' '%s' '%s' '%s' '%s' '%s' '%s' '%s'" > /var/tmp/tmpsu'  """ % (node,xFilename,yFilename,EFilename,SFilename,foldIndex,sopC,outputFilename,logFilename,stepSize1,stepSize2,isTest) )
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
  '''
  a wrapper function to generate cluster node with good perforamnce, to define a job space, and to launch jobs on computing node of the cluster
  '''
  logging.info('\t\tGenerating priority queue.')
  paramInd = 0
  kFold    = 5 
  suffix   = 'sel'
  isTest   = '0'
  # iterate over the lists
  xFilenameList         = ['../Data/tcdb.all.KUNIMKL','../Data/tcdb.all.KALIGN','../Data/tcdb.all.KALIGNF']
  foldIndexList         = xrange(1,kFold+1) 
  cList                 = ['1000','5000','10000','50000']
  stepSize1List         = ['7','9','11']
  stepSize2List         = ['7','9','11']
  cList.reverse()
  stepSize1List.reverse()
  stepSize2List.reverse()

  yFilename   = '../Data/tcdb.TC'
  EFilename   = '../Data/tcdb.TC.E'
  SFilename   = '../Data/tcdb.TC.SrcSpc'

  for xFilename,foldIndex,sopC,stepSize1,stepSize2 in list(itertools.product(xFilenameList,foldIndexList,cList,stepSize1List,stepSize2List)):
    tmpDir   = '../ResultsSOP/tmp_%s_%s/' % ( re.sub('.*/','',xFilename), re.sub('.*/','',yFilename))
    if not os.path.exists(tmpDir): os.mkdir(tmpDir)
    paramInd += 1
    outputFilename = tmpDir + '/' + re.sub('.*/','',xFilename) + '_' + re.sub('.*/','',yFilename) + '_f' + str(foldIndex) + '_c' +sopC + '_s1' + stepSize1 + '_s2' + stepSize2 + '_t' + isTest + '_' + suffix + '.mat'
    logFilename = tmpDir + '/' + re.sub('.*/','',xFilename) + '_' + re.sub('.*/','',yFilename) + '_f' + str(foldIndex) + '_c' +sopC + '_s1' + stepSize1 + '_s2' + stepSize2 + '_t' + isTest + '_' + suffix + '.log'
    ## check if result is ready already
    if checkfile(outputFilename): continue
    ## put parameter into queue
    job_queue.put( (paramInd,(str(paramInd),xFilename,yFilename,EFilename,SFilename,str(foldIndex),sopC,outputFilename,logFilename,stepSize1,stepSize2,isTest,suffix)) )

  # get computing node
  logging.info('\t\tObtain cluster node')
  cluster = get_free_nodes()[0]
  #cluster = ['ukko133'] 

  # run jobs
  job_size = job_queue.qsize()
  logging.info( "\t\tProcessing %d job_queue" % (job_size))
  is_main_run_factor=1
  # running job_queue
  threads = []
  workerload = 1 
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
  '''
  the definition of __name__ is to wrap up some computation so that they would be executed when the function is loaded as a module
  '''
  run()
  pass


