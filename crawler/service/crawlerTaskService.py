#coding=utf-8

import threading
import random
import time
from downloadData import saveData
import logging
from browserService import check_key,check_status_by_key

logger=logging.getLogger('django')

def startTask(key):
    logger.info(u'启动爬虫任务')
    check_key(key)
    threading._start_new_thread
    threading._start_new_thread(prepareTask,(key,))

def prepareTask(key):
    logger.info(u'开始前准备...')
    time.sleep(10)
    logger.info(u'开始爬虫任务')
    runTask(key)

def runTask(key):
    time.sleep(5)
    logger.info(u'爬虫定时任务开始')
    saveData(key)
    logger.info(u'本次爬虫定时任务完成')
    time.sleep(random.randint(10,30))
    # check_status_by_key(key)
    threading.Timer(random.randint(10,30),runTask(key))

