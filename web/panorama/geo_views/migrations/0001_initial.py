# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-20 11:13
from __future__ import unicode_literals

from django.db import migrations

from django.conf import settings

from geo_views import migrate


def create_site(apps, *args, **kwargs):
    Site = apps.get_model('sites', 'Site')
    Site.objects.create(
        domain=settings.DATAPUNT_API_URL,
        name='API Domain'
    )


def delete_site(apps, *args, **kwargs):
    Site = apps.get_model('sites', 'Site')
    Site.objects.filter(name='API Domain').delete()


class Migration(migrations.Migration):

    dependencies = [
            ('sites', '0001_initial'),
            ('panoramas', '0001_initial')
    ]

    operations = [
        migrations.RunPython(code=create_site, reverse_code=delete_site),

        migrate.ManageView(
            view_name="geo_panoramas_panoramafotopunt",
            sql="""
SELECT
    pp.id,
    pp.pano_id as display,
    pp.roll,
    pp.pitch,
    pp.heading,
    pp.timestamp,
    pp.geolocation AS geometrie,
    'https://acc.atlas.amsterdam.nl/panorama' || pp.path || '/' ||
    pp.filename AS url,
    site.domain || 'panoramas/opnamelocatie/' || pp.pano_id || '/' AS uri
FROM
    panoramas_panorama pp,
    django_site site
WHERE
    site.name = 'API Domain'
AND
    pp.geolocation IS NOT NULL
"""
        ),

    ]
