from time import sleep
import random
from threading import Thread
from threading import Lock

printLock = Lock()
resourceLock = Lock()
readerLock = Lock()
list1 = [3, 4, 5]
read_count =0

def wTask(tnum):
  resourceLock.acquire() #works as wait from solution

  with printLock:
    print ('Starting w thread: {}'.format(tnum))
  sleep(3) #represnts writing process
  with printLock:
    print('Leaving w thread: {}'.format(tnum))

  resourceLock.release() #works as signal with mutex

def rTask(tnum):
  global read_count
  readerLock.acquire()
  read_count+=1
  if read_count == 1:
    resourceLock.acquire()
  readerLock.release()

  with printLock:
    print ('Starting r thread: {}'.format(tnum))
  sleep(random.choice(list1))
  with printLock:
    print('Leaving r thread: {}'.format(tnum))

  readerLock.acquire()
  read_count -= 1
  if read_count == 0:
    resourceLock.release()
  readerLock.release()

numofW = 0
numofR = 0
writersmade=0
readersmade = 0
thread = []
for i in range(20):
  if i== 0 or i%10 == 0:
    thread.append(Thread(target=wTask, args=(i,)))
    numofW+=1
    writersmade+=1
  else:
    thread.append(Thread(target=rTask, args=(i,)))
    numofR+=1
    readersmade+=1
  thread[i].start()
with printLock:
  print('Waiting for the threads to finish...')
sleep(2)
for i in range(20):
  with printLock:
    print('Waiting for thread {} to finish...'.format(i))
  thread[i].join()
  if i== 0 or i%10 == 0:
    numofW-=1
  else:
    numofR-=1
  with printLock:
    print('Thread {} joined...'.format(i))
with printLock:
  print('waiting done')

print("Writers waiting: " , numofW , " Readers waiting: " , numofR)
print("writers made:" , writersmade, " Readers made: ", readersmade)

