# Generated by Django 5.1.3 on 2024-11-12 18:46

import django.contrib.gis.db.models.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("quality_of_life", "0003_mark_location_existing"),
    ]

    operations = [
        migrations.CreateModel(
            name="KindOfAppeal",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "kind_of_appeal_id",
                    models.IntegerField(db_column="kind_of_appeal_id", unique=True),
                ),
                ("name_en", models.CharField(db_column="name_en", max_length=255)),
                ("name_ru", models.CharField(db_column="name_ru", max_length=255)),
                ("name_kk", models.CharField(db_column="name_kk", max_length=255)),
                ("is_active", models.BooleanField(db_column="is_active")),
            ],
            options={
                "db_table": "kind_of_appeal",
                "managed": False,
            },
        ),
        migrations.RemoveField(
            model_name="additionalattributes",
            name="kind_of_appea_id",
        ),
        migrations.AddField(
            model_name="appeal",
            name="hexagon_id",
            field=models.IntegerField(blank=True, db_column="hexagon_id", null=True),
        ),
        migrations.AddField(
            model_name="appeal",
            name="index_right",
            field=models.IntegerField(blank=True, db_column="index_right", null=True),
        ),
        migrations.AddField(
            model_name="appeal",
            name="location",
            field=django.contrib.gis.db.models.fields.PointField(
                geography=True, null=True, srid=4326
            ),
        ),
        migrations.AddField(
            model_name="additionalattributes",
            name="kind_of_appeal_id",
            field=models.ForeignKey(
                db_column="kind_of_appeal_id",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="quality_of_life.kindofappeal",
            ),
        ),
    ]