#coding=utf-8
import logging
from django.core.cache import cache
import os



logger=logging.getLogger('django')

def check_browser_state():
    if __get_browser_state():
        try:
            os.system("ps -ef | grep phantomjs | grep -v grep | awk '{print $2}' | xargs kill -9")
        except Exception as e:
            logger.error(u'os关闭浏览器失败：'+e.message)

def save_browser_open_state():
    try:
        cache.set('browser_state',True)
    except Exception as e:
        logger.error(u'保存浏览器状态（开启）异常:'+e.message)

def save_browser_close_state():
    try:
        cache.set('browser_state',False)
    except Exception as e:
        logger.error(u'保存浏览器状态（关闭）异常:' + e.message)

def __get_browser_state():
    try:
        return cache.get('browser_state')
    except Exception as e:
        logger.error(u'获取浏览器状态异常:'+e.message)