# Generated by Django 4.2.5 on 2023-09-11 22:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data_collection_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='response',
            name='submission_date',
        ),
    ]
