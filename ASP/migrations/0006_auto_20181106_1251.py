# Generated by Django 2.1.2 on 2018-11-06 04:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ASP', '0005_auto_20181105_2329'),
    ]

    operations = [
        migrations.AddField(
            model_name='supply',
            name='image',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='order',
            name='dispatchTime',
            field=models.DateTimeField(default=datetime.datetime(2018, 11, 6, 12, 51, 50, 11002)),
        ),
        migrations.AlterField(
            model_name='order',
            name='placeTime',
            field=models.DateTimeField(default=datetime.datetime(2018, 11, 6, 12, 51, 50, 11002)),
        ),
    ]
