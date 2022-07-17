# ensure app is imported when Django starts.
# so shared_task will use this app

from .celery import app as celery_app

__all__ = ("celery_app",)
