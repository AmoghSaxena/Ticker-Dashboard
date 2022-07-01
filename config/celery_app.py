import os
from celery import Celery
from config.settings import base
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

app = Celery("setup")

app.conf.timezone = base.TIME_ZONE

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


app.conf.beat_schedule = {
    "check_pending_upload": {
        "task": "ipad_config.views.upload_task",
        "schedule": 20.0
    },
    "export_ipad_configuration_task": {
        "task": "ipad_config.views.export_ipad_configuration_task",
        "schedule": 20.0
    }

}


