from __future__ import absolute_import

from celery import task
from crawler.service.crawlerTaskService import *
import logging



logger=logging.getLogger('django')

@task
def newsCrawler():
    addNewsCrawler()

@task
def proxyIpCrawler():
    addProxyCrawler()

@task
def runTask():
    runTaskCache()


