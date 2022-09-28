# Generated by Django 4.0.6 on 2022-09-29 10:06
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("SRS", "0004_delete_test2_test2q_1_delete_test3_test3q_1_and_more"),
    ]

    operations = [
        migrations.DeleteModel(
            name="AS91578_Q_1",
        ),
        migrations.DeleteModel(
            name="Test2_Q_1",
        ),
        migrations.DeleteModel(
            name="Test3_Q_1",
        ),
        migrations.DeleteModel(
            name="Test_Q_1",
        ),
        migrations.CreateModel(
            name="AS2_Q_1",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("SRS.qaa",),
        ),
        migrations.CreateModel(
            name="AS3_Q_1",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("SRS.qaa",),
        ),
        migrations.CreateModel(
            name="AS4_Q_1",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("SRS.qaa",),
        ),
        migrations.CreateModel(
            name="AS90521_Q_1",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("SRS.qaa",),
        ),
    ]
