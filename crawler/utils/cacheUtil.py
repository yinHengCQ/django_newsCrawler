#coding=utf-8
from django.core.cache import cache


def load_job51_cache(job_51_id):
    try:temp=cache.get(job_51_id)
    except:temp=None
    return temp

def save_job51_sql_id(job_51_id,sql_ids):
    try:cache.set(job_51_id,sql_ids)
    except:pass
