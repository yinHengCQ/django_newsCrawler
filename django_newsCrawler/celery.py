from __future__ import absolute_import

import os

from celery import Celery,platforms
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_newsCrawler.settings')

app = Celery('django_newsCrawler')
platforms.C_FORCE_ROOT=True

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
