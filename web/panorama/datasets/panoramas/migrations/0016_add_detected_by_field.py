# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-14 12:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panoramas', '0015_readd_index_to_mv'),
    ]

    operations = [
        migrations.AddField(
            model_name='region',
            name='detected_by',
            field=models.CharField(default=None, max_length=255),
            preserve_default=False,
        ),
    ]