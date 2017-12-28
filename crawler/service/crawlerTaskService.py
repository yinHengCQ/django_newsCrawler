#coding=utf-8

import threading
import random
import time
from downloadData import saveData
import logging

logger=logging.getLogger('django')

def startTask():
    logger.info(u'启动爬虫任务')
    threading._start_new_thread(prepareTask,())

def prepareTask():
    logger.info(u'开始前准备...')
    time.sleep(10)
    logger.info(u'开始爬虫任务')
    runTask()

def runTask():
    logger.info(u'爬虫定时任务开始')
    saveData()
    logger.info(u'本次爬虫定时任务完成')
    time.sleep(random.randint(10,30))
    threading.Timer(random.randint(10,30),runTask())

