# Generated by Django 4.0.6 on 2022-10-05 14:46
import datetime

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("SRS", "0007_remove_assesment_attempts"),
    ]

    operations = [
        migrations.AddField(
            model_name="assesment",
            name="last_accessed",
            field=models.DateTimeField(default=datetime.datetime.now, null=True),
        ),
    ]
