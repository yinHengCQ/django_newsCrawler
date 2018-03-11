from __future__ import absolute_import

from celery import task
from crawler.service.crawlerTaskService import *
from crawler.service.urllib_download_data import download_51job



@task
def newsCrawler():
    addNewsCrawler()

@task
def proxyIpCrawler():
    addProxyCrawler()

@task
def job51Crawler():
    addJob51Crawler()

@task
def job51DetailCrawler():
    addJob51DetailCrawler()

@task
def runTask():
    runTaskCache()

@task
def urllib_51_crawler():
    download_51job()




