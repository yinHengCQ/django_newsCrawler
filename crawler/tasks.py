from __future__ import absolute_import

from celery import task
from crawler.service.crawlerTaskService import *
from crawler.service.urllib_download_data import download_51job
from crawler.service.urlib_download_58resume import download_data
from crawler.service.urllib_download_ganjiresume import download_ganji_data
import os,logging

__logger=logging.getLogger('django')

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

@task
def scrapy_all_job51():
    os.system("cd C:/Users/Administrator/PycharmProjects/django_newsCrawler/crawler/scrapy_crawler && scrapy crawl job51_crawler")

@task
def urlib_58_resume(base_url,begin_index,end_index):
    __logger.info('base_url:{0};begin_index:{1};end_index:{2}'.format(base_url,begin_index,end_index))
    # download_data("http://cq.58.com/searchjob/pn1")
    for index in range(begin_index,end_index+1):
        download_data(base_url.format(index))

@task
def urlib_ganji_resume(list_str):
    __logger.info('city_codes:{0}'.format(list_str))
    for var in eval(list_str):
        download_ganji_data(var)