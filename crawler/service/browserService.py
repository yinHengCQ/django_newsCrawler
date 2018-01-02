#coding=utf-8
from crawler.models import browserRecord
import logging
import os

logger=logging.getLogger('django')

def __get_status_by_key(key):
    try:
        try:
            orgin =browserRecord.objects.get(key=key)
        except browserRecord.DoesNotExist:
            orgin =browserRecord.objects.create(key=key, status=False, totleFail=0)
        return orgin.status
    except Exception as e:
        logger.error(u'获取浏览器当前状态异常:'+e.message)
        return True

def save_open_status(key):
    try:
        obj=browserRecord.objects.get(key=key)
        obj.status = True
        obj.save()
    except Exception as e:
        logger.error(u'保存浏览器状态异常（开启状态）:' + e.message)

def save_cloes_status(key):
    try:
        obj = browserRecord.objects.get(key=key)
        obj.status = False
        obj.save()
    except Exception as e:
        logger.error(u'保存浏览器状态异常（关闭状态）:' + e.message)

def __add_fail_count_key(key):
    try:
        obj = browserRecord.objects.get(key=key)
        obj.totleFail=obj.totleFail+1
        obj.save()
    except Exception as e:
        logger.error(u'保存浏览器失败记录异常:' + e.message)

def check_status_by_key(key):
    if __get_status_by_key(key):
        __add_fail_count_key(key)
        try:
            os.system("ps -ef | grep phantomjs | grep -v grep | awk '{print $2}' | xargs kill -9")
        except Exception as e:
            logger.error(u'os关闭浏览器失败，key:'+key+u"异常信息："+e.message)