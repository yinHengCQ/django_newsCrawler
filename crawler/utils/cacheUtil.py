#coding=utf-8
from django.core.cache import cache


def is_job_id_exists(job_id):
    cache_data=cache.get('51job{0}'.format(job_id))
    if cache_data == None: cache.set('51job{0}'.format(job_id), 1);return True
    else:False