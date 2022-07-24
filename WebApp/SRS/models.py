from django.db import models

from django.db.models.signals import pre_delete
from django.contrib.sessions.models import Session
from django.dispatch import receiver


def next(self, subject: str):
    pass


def return_to_queue(self):
    pass


@receiver(pre_delete)  # sender=Session, dispatch_uid="session_delete_signal")
def session_end_handler(sender, instance, using, **kwargs):
    """Forced cleanup for when a session ends and ensures that questions are returned into the queue. Called in models.py"""
    if sender == Session:
        print(f"session {kwargs.get('instance').session_key} ended")
