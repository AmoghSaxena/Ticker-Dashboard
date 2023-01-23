from __future__ import unicode_literals,absolute_import
import os

from celery import Celery
from django.conf import settings
from celery.schedules import crontab
from ticker_dashboard.settings import TIME_ZONE

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ticker_dashboard.settings")

app=Celery('ticker_dashboard')
app.conf.enable_utc=False

app.conf.update(timezone=TIME_ZONE)

app.config_from_object(settings,namespace='CELERY')

#Celery Beat
app.autodiscover_tasks()

app.conf.beat_schedule = {
}

@app.task(bind=True)
def debug_task(self):
    print('Request: {}'.format(self.request))
    