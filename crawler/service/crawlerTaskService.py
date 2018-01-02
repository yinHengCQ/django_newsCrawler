#coding=utf-8

import random
import time
from downloadData import saveData
import logging
from browserService import check_status_by_key

logger=logging.getLogger('django')

def runNewsCrawler(key):
    logger.info(u'启动新闻爬虫')
    time.sleep(random.randint(1,10))
    saveData(key)
    check_status_by_key(key)
    logger.info(u'本次新闻爬虫完成')

