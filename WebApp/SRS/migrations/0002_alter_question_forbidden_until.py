# Generated by Django 4.0.6 on 2022-08-17 10:12
import datetime

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("SRS", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="question",
            name="forbidden_until",
            field=models.DateTimeField(default=datetime.datetime(1, 1, 1, 0, 0)),
        ),
    ]
