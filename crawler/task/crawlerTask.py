#coding=utf-8
from crawler.service.crawlerTaskService import startTask

def newsCrawle():
    startTask('http://business.sohu.com/')