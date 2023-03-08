import queue
import random


class Printer:
    '''
    tracks whether the printer has a current task, if it is busy and the amount of time needed can be computed from the number of pages in the task.
    '''

    def __init__(self, ppm):
        # allows the pages-per-minute
        self.pagerate = ppm
        self.currentTask = None
        self.timeRemaining = 0

    def tick(self):
        # decrements the internal timer and sets the printer to idle if the task is completed
        if self.currentTask != None:
            self.timeRemaining = self.timeRemaining - 1
            if self.timeRemaining <= 0:
                self.currentTask = None

    def busy(self):
        if self.currentTask != None:
            return True
        else:
            return False

    def startNext(self, newtask):
        self.currentTask = newtask
        self.timeRemaining = newtask.getPages() * 60/self.pagerate


class Task:
    '''
    represents a single printing task. when the task is created, a random number generator will provide a length from 1 to 20 pages. randrange from random module will do this.
    '''

    def __init__(self, time):
        self.timestamp = time
        self.pages = random.randrange(1, 21)

    def getStamp(self):
        # each task will need a timestamp to be used for computing waiting time. this represents the time that the task was created and place in the printer queue
        return self.timestamp

    def getPages(self):
        return self.pages

    def waitTime(self, currenttime):
        # used to retrieve the amount of time spent in the queue before printing
        return currenttime - self.timestamp


def simulation(numSeconds, pagesPerMinute):

    labprinter = Printer(pagesPerMinute)
    printQueue = queue.Queue()
    waitingtimes = []

    for currentSecond in range(numSeconds):
         # decides whether a new printing task has been created
        if newPrintTask():
            task = Task(currentSecond)
            printQueue.put(task)

        if (not labprinter.busy()) and (not printQueue.empty()):
            nexttask = printQueue.get()
            waitingtimes.append(nexttask.waitTime(currentSecond))
            labprinter.startNext(nexttask)

        labprinter.tick()

    averageWait = sum(waitingtimes)/len(waitingtimes)
    print("Average Wait %6.2f seconds %3d tasks remaining." % (averageWait, printQueue.qsize()))


def newPrintTask():
   
    num = random.randrange(1, 181)
    # return a random integer between 1 and 180, print tasks arrive once every 180 seconds.
    if num == 180:
        return True
    else:
        return False


for i in range(10):
    simulation(3600, 5)
