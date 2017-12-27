#coding=utf-8

import threading
import random
import time
from downloadData import saveData


def startTask():
    threading._start_new_thread(prepareTask,())

def prepareTask():
    time.sleep(10)
    runTask()

def runTask():
    print 'start crawler task...'
    saveData()
    print 'crawler task finish!'
    time.sleep(random.randint(10,30))
    runTask()

