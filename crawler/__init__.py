from django.core.cache import cache
import logging


logger=logging.getLogger('django')
try:
    cache.set('browser_state',False)
except Exception as e:
    logger.error('init redis data error:'+e.message)