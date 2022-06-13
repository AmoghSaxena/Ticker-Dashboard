from __future__ import absolute_import,unicode_literals
import os
from celery.schedules import crontab

from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "celerychecking.settings")

app = Celery("celerychecking")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

@app.task(bind=False)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

app.conf.beat_schedule = {
    'print-time-twenty-seconds': {
        'task': 'print_time',
        'schedule': 40.0, 
    },
    'execute_command':{
        'task' : 'execute_command',
        'schedule' : 40.0
    }
}