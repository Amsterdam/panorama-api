# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-11-12 12:23
from __future__ import unicode_literals

from datetime import datetime

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panoramas', '0033_readd_recent_adjacencies'),
    ]

    operations = [
        migrations.AlterField(
            model_name='panorama',
            name='mission_year',
            field=models.IntegerField(db_index=True, default=datetime.now().year),
        ),
        migrations.AlterField(
            model_name='panorama',
            name='surface_type',
            field=models.CharField(db_index=True, choices=[('L', 'land'), ('W', 'water')], default='L', max_length=1),
        ),
        migrations.AlterField(
            model_name='panorama',
            name='mission_type',
            field=models.TextField(db_index=True, default='bi', max_length=16),
        ),
        migrations.AlterField(
            model_name='panorama',
            name='mission_distance',
            field=models.IntegerField(db_index=True, default=5),
            preserve_default=False,
        ),
    ]