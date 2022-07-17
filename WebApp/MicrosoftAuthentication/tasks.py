# WebApp/MicrosoftAuthentication/tasks.py

from celery import shared_task
from django.core import management


@shared_task
def session_cleanup():
    # cleanup expired session by using Django management command.
    management.call_command("clearsessions", verbosity=0)
