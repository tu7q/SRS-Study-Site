#
# celery.py

import os
from celery import Celery

# Set default django settings module for 'celery' program
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "WebApp.settings")

app = Celery("WebApp")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f"Requests: {self.request!r}")
