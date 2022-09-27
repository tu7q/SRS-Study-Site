from django.db.models.signals import post_save
from django.dispatch import receiver
from SRS.models import Assesment
from SRS.models import QAA


@receiver(post_save)
def create_questions(sender, instance, created, **kwargs):
    if not isinstance(instance, Assesment):
        return
    if created:
        for q_model in QAA.ALL[instance.__class__]:
            q_model.objects.create(assesment=instance)
