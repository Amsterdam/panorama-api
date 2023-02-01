# Generated by Django 2.1.5 on 2019-02-18 10:57

import django.contrib.gis.db.models.fields
import django.contrib.postgres.fields
from django.db import migrations, models
import django.utils.timezone
import datasets.migrate
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    operations = [
        migrations.CreateModel(
            name="Mission",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.TextField(max_length=24, unique=True)),
                ("date", models.DateField(null=True)),
                ("neighbourhood", models.TextField(max_length=50, null=True)),
                ("mission_type", models.TextField(default="bi", max_length=16)),
                ("mission_year", models.IntegerField(max_length=4, null=True)),
                (
                    "surface_type",
                    models.CharField(
                        choices=[("L", "land"), ("W", "water")],
                        default="L",
                        max_length=1,
                    ),
                ),
                ("mission_distance", models.IntegerField(default=5)),
            ],
        ),
        migrations.CreateModel(
            name="Panorama",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "pano_id",
                    models.CharField(db_index=True, max_length=37, unique=True),
                ),
                ("timestamp", models.DateTimeField()),
                ("filename", models.CharField(max_length=255)),
                ("path", models.CharField(max_length=400)),
                (
                    "geolocation",
                    django.contrib.gis.db.models.fields.PointField(dim=3, srid=4326),
                ),
                ("roll", models.FloatField()),
                ("pitch", models.FloatField()),
                ("heading", models.FloatField()),
                (
                    "_geolocation_2d",
                    django.contrib.gis.db.models.fields.PointField(
                        default=None, null=True, srid=4326
                    ),
                ),
                (
                    "status",
                    model_utils.fields.StatusField(
                        choices=[(0, "dummy")],
                        default="to_be_rendered",
                        max_length=100,
                        no_check_for_status=True,
                        verbose_name="status",
                    ),
                ),
                (
                    "status_changed",
                    model_utils.fields.MonitorField(
                        default=django.utils.timezone.now,
                        monitor="status",
                        verbose_name="status changed",
                    ),
                ),
                (
                    "mission_type",
                    models.TextField(db_index=True, default="bi", max_length=16),
                ),
                (
                    "_geolocation_2d_rd",
                    django.contrib.gis.db.models.fields.PointField(
                        default=None, null=True, srid=28992
                    ),
                ),
                ("mission_year", models.IntegerField(db_index=True, default=2019)),
                (
                    "surface_type",
                    models.CharField(
                        choices=[("L", "land"), ("W", "water")],
                        db_index=True,
                        default="L",
                        max_length=1,
                    ),
                ),
                ("mission_distance", models.IntegerField(db_index=True, default=5)),
                (
                    "tags",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(max_length=32),
                        blank=True,
                        db_index=True,
                        default=[],
                        size=None,
                    ),
                ),
            ],
            options={
                "ordering": ("id",),
            },
        ),
        migrations.CreateModel(
            name="Traject",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("timestamp", models.DateTimeField()),
                (
                    "geolocation",
                    django.contrib.gis.db.models.fields.PointField(dim=3, srid=4326),
                ),
                ("north_rms", models.DecimalField(decimal_places=14, max_digits=20)),
                (
                    "east_rms",
                    models.DecimalField(
                        blank=True, decimal_places=14, max_digits=20, null=True
                    ),
                ),
                (
                    "down_rms",
                    models.DecimalField(
                        blank=True, decimal_places=14, max_digits=20, null=True
                    ),
                ),
                ("roll_rms", models.FloatField(blank=True, null=True)),
                ("pitch_rms", models.FloatField(blank=True, null=True)),
                ("heading_rms", models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Region",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "region_type",
                    models.CharField(
                        choices=[("N", "Nummerbord"), ("G", "Gezicht")], max_length=1
                    ),
                ),
                ("left_top_x", models.IntegerField()),
                ("left_top_y", models.IntegerField()),
                ("right_top_x", models.IntegerField()),
                ("right_top_y", models.IntegerField()),
                ("left_bottom_x", models.IntegerField()),
                ("left_bottom_y", models.IntegerField()),
                ("right_bottom_x", models.IntegerField()),
                ("right_bottom_y", models.IntegerField()),
                ("detected_by", models.CharField(default=None, max_length=255)),
                ("pano_id", models.CharField(db_index=True, default="", max_length=37)),
            ],
            options={
                "ordering": ("id",),
            },
        ),
        datasets.migrate.ManageView(
            view_name="panoramas_adjacencies_new",
            sql="""
                SELECT
                    id,
                    from_pano_id,
                    to_pano_id AS pano_id,

                    to_filename AS filename,
                    to_path AS path,
                    to_surface_type AS surface_type,
                    to_mission_type AS mission_type,
                    to_mission_distance AS mission_distance,
                    to_mission_year AS mission_year,
                    to_tags AS tags,
                    to_timestamp AS timestamp,

                    to_status AS status,
                    to_status_changed AS status_changed,

                    relative_distance,
                    relative_heading,
                    degrees(atan2(relative_elevation, relative_distance)) AS relative_pitch,
                    relative_elevation,

                    from_geolocation_2d_rd,

                    to_geolocation_2d_rd AS _geolocation_2d_rd,
                    to_geolocation_2d AS _geolocation_2d,
                    to_geolocation AS geolocation
                FROM (SELECT
                        from_pano.id || '-' || to_pano.id AS id,

                        from_pano.pano_id AS from_pano_id,
                        to_pano.pano_id AS to_pano_id,

                        to_pano.filename AS to_filename,
                        to_pano.path AS to_path,
                        to_pano.surface_type AS to_surface_type,
                        to_pano.mission_type AS to_mission_type,
                        to_pano.mission_distance AS to_mission_distance,
                        to_pano.mission_year AS to_mission_year,
                        to_pano.tags AS to_tags,
                        to_pano.timestamp AS to_timestamp,

                        to_pano.status AS to_status,
                        to_pano.status_changed AS to_status_changed,

                        ST_Distance(geography(to_pano.geolocation),
                            geography(from_pano.geolocation)) AS relative_distance,
                        degrees(ST_Azimuth(geography(from_pano.geolocation),
                            geography(to_pano.geolocation))) AS relative_heading,
                        ST_Z(to_pano.geolocation) - ST_Z(from_pano.geolocation)
                            AS relative_elevation,

                        from_pano._geolocation_2d_rd AS from_geolocation_2d_rd,

                        to_pano._geolocation_2d_rd AS to_geolocation_2d_rd,
                        to_pano._geolocation_2d AS to_geolocation_2d,
                        to_pano.geolocation AS to_geolocation
                    FROM
                        panoramas_panorama from_pano,
                        panoramas_panorama to_pano
                    WHERE
                        to_pano.status = 'done'
                    ) subquery1
            """,
        ),
    ]
