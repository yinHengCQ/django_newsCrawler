#coding=utf-8
from djcelery.models import PeriodicTask
import logging


logger=logging.getLogger('django')

def getCrawlerInfo():
    try:
        return PeriodicTask.objects.filter(crontab__isnull=True).exclude(name='runTask')
    except Exception as e:
        logger.error(u'获取爬虫状态异常：'+e.message)
        return None