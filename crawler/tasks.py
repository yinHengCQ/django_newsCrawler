from __future__ import absolute_import

from celery import task
from crawler.service.crawlerTaskService import *
from crawler.service.urllib_download_data import download_51job
from crawler.service.urlib_download_58resume import download_data
import os


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
def urlib_58_resume():
    download_data("http://cq.58.com/searchjob/pn1")

