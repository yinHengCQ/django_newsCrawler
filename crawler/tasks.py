from __future__ import absolute_import

from celery import task
from crawler.service.crawlerTaskService import runNewsCrawler



@task
def newsCrawler():
    runNewsCrawler('http://business.sohu.com/')


