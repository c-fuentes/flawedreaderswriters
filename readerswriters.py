from time import sleep
import random
from threading import Thread
from threading import Lock

#group of variables 
printLock = Lock()
resourceLock = Lock()
readerLock = Lock()
list1 = [3, 4, 5]
read_count = 0


#Simulates a writer attempting to write something in the OS 
def wTask(tnum):
  resourceLock.acquire() #works as wait

  with printLock:
    print ('Starting w thread: {}'.format(tnum))
  sleep(3) #represnts writing process
  with printLock:
    print('Leaving w thread: {}'.format(tnum))

  resourceLock.release() #works as signal with mutex

#Simulates the reader trying to read data in the OS
def rTask(tnum):
  global read_count
  readerLock.acquire() #Makes sure only one reader is messing with the reader count
  read_count+=1 
  if read_count == 1: #The first reader will hog the resource lock
    resourceLock.acquire()
  readerLock.release() #Allows other readers to mess with the reader count

  with printLock:
    print ('Starting r thread: {}'.format(tnum))
  sleep(random.choice(list1)) #reader sleeps for a random amt of time(Decided by the array list1)
  with printLock:
    print('Leaving r thread: {}'.format(tnum))

  readerLock.acquire() 
  read_count -= 1
  if read_count == 0: #the resource will only be released when there are no more readers using the resource
    resourceLock.release()
  readerLock.release()
#The reason this "solution" is NOT a valid solution to the readers writers problem is that readers WILL keep the resource lock
#Even when writers are "next" in line. 
#That happens since the resourceLock will only be released when no more readers are being created 
#because otherwise readers will always be allowed in the resource after the first.
#In conclusion, to solve this flawed solution there must be a way to stop more readers from entering when a writer is next in line.


#Testing 
numofW = 0
numofR = 0
writersmade = 0
readersmade = 0
thread = []
for i in range(20):
  if i == 0 or i%10 == 0: #Insures a ratio of 1 writer to 9 readers
    thread.append(Thread(target=wTask, args=(i,))) #Creates writer thread
    numofW+=1
    writersmade+=1
  else:
    thread.append(Thread(target=rTask, args=(i,))) #Creates reader thread
    numofR+=1
    readersmade+=1
  thread[i].start() #Starts the thread and function of the determined writer/reader
with printLock:
  print('Waiting for the threads to finish...')

sleep(2)

for i in range(20):
  with printLock:
    print('Waiting for thread {} to finish...'.format(i))
  thread[i].join() #"Closes" the thread
  if i== 0 or i%10 == 0: #Determines if it decreases the number of readers or writers using the same "formula" that created them
    numofW-=1
  else:
    numofR-=1
  with printLock:
    print('Thread {} joined...'.format(i))
with printLock:
  print('waiting done')

print("Writers waiting: " , numofW , " Readers waiting: " , numofR)
print("writers made:" , writersmade, " Readers made: ", readersmade)

