# Generated by Django 2.1.2 on 2018-11-05 13:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ASP', '0002_auto_20181105_1810'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='time',
        ),
        migrations.AddField(
            model_name='order',
            name='dispatchTime',
            field=models.DateTimeField(default=datetime.datetime(2018, 11, 5, 21, 8, 46, 445577)),
        ),
        migrations.AddField(
            model_name='order',
            name='placeTime',
            field=models.DateTimeField(default=datetime.datetime(2018, 11, 5, 21, 8, 46, 445577)),
        ),
    ]
