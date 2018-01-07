#coding=utf-8


from downloadData import startCrawler
import logging
from django.core.cache import cache
from browserService import check_browser_state


__logger=logging.getLogger('django')

def addNewsCrawler():
    __logger.info(u'添加新闻爬虫任务')
    try:
        orgin = cache.get('task_list')
        if orgin==None:
            orgin=[]
        orgin.append('newsCrawler')
        cache.set('task_list', orgin)
    except Exception as e:
        __logger.error(u'添加新闻爬虫任务异常：'+e.message)

def addProxyCrawler():
    __logger.info(u'添加代理IP爬虫任务')
    try:
        orgin = cache.get('task_list')
        if orgin==None:
            orgin=[]
        orgin.append('proxyIpCrawler')
        cache.set('task_list', orgin)
    except Exception as e:
        __logger.error(u'添加代理IP爬虫任务异常：'+e.message)

def addJob51Crawler():
    __logger.info(u'添加51job爬虫任务')
    try:
        orgin = cache.get('task_list')
        if orgin==None:
            orgin=[]
        orgin.append('job51Crawler')
        cache.set('task_list', orgin)
    except Exception as e:
        __logger.error(u'添加51job爬虫任务异常：'+e.message)


def runTaskCache():
    try:
        __logger.info(u'开始爬虫任务...')
        startCrawler()
    except Exception as e:
        __logger.error(u'爬虫任务异常：' + e.message)
        check_browser_state()