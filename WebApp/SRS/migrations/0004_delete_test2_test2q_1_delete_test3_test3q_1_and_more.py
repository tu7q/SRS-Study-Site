# Generated by Django 4.0.6 on 2022-09-20 16:22
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("SRS", "0003_delete_q_1_delete_test2q_1_delete_test3q_1_and_more"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Test2_Test2Q_1",
        ),
        migrations.DeleteModel(
            name="Test3_Test3Q_1",
        ),
        migrations.DeleteModel(
            name="Test_TestQ_1",
        ),
        migrations.CreateModel(
            name="Test2_Q_1",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("SRS.qaa",),
        ),
        migrations.CreateModel(
            name="Test3_Q_1",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("SRS.qaa",),
        ),
        migrations.CreateModel(
            name="Test_Q_1",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("SRS.qaa",),
        ),
    ]
