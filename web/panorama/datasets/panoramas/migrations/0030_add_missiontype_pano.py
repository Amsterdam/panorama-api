# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-11-12 12:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panoramas', '0029_add_mission_attribs'),
    ]

    operations = [
        migrations.AddField(
            model_name='panorama',
            name='mission_year',
            field=models.TextField(max_length=4, null=True),
        ),
        migrations.AddField(
            model_name='panorama',
            name='surface_type',
            field=models.CharField(choices=[('L', 'land'), ('W', 'water')], default='L', max_length=1),
        ),
        migrations.AlterField(
            model_name='panorama',
            name='mission_type',
            field=models.TextField(default='bi', max_length=16),
        ),
    ]
