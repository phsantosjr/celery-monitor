# -*- coding: utf-8 -*-
#!/bin/python
from __future__ import absolute_import
from django.conf import settings
from multiprocessing import current_process
import os
from celery import Celery
from celery.signals import worker_process_init

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'celerymonitor.settings')

app = Celery('celerymonitor')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.conf.update(
    CELERY_ACCEPT_CONTENT=['json'],
    CELERY_TASK_SERIALIZER='json',
    CELERY_RESULT_SERIALIZER='json'
)


@worker_process_init.connect
def fix_multiprocessing(**kwargs):
    """
    This is a known issue with celery. It stems from an issue introduced in the billiard dependency.
    A work-around is to manually set the _config attribute for the current process.
    Thanks to user @martinth for the work-around below.
    https://github.com/celery/celery/issues/1709#issuecomment-122467424
    https://stackoverflow.com/questions/27904162/using-multiprocessing-pool-from-celery-task-raises-exception
    """
    try:
        current_process()._config
    except AttributeError:
        current_process()._config = {'semprefix': '/mp'}
