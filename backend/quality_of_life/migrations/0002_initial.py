# Generated by Django 5.1.3 on 2024-11-09 15:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("quality_of_life", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Appeal",
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
                ("title", models.TextField(db_column="title")),
                (
                    "description",
                    models.TextField(blank=True, db_column="description", null=True),
                ),
                ("creation_date", models.DateTimeField(db_column="creation_date")),
                ("completion_date", models.DateTimeField(db_column="completion_date")),
                ("status", models.IntegerField(db_column="status")),
                ("process_status", models.IntegerField(db_column="process_status")),
                ("address", models.TextField(db_column="address")),
                ("coord_x", models.FloatField(db_column="coord_x")),
                ("coord_y", models.FloatField(db_column="coord_y")),
            ],
            options={
                "db_table": "appeals",
            },
        ),
        migrations.CreateModel(
            name="AdditionalAttributes",
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
                    "received_from",
                    models.CharField(db_column="received_from", max_length=255),
                ),
                ("category_id", models.IntegerField(db_column="category_id")),
                ("kind_of_appea_id", models.IntegerField(db_column="kind_of_appea_id")),
                (
                    "budgetary_funds_are_required",
                    models.BooleanField(db_column="budgetary_funds_are_required"),
                ),
                (
                    "appeal",
                    models.ForeignKey(
                        db_column="appeal_id",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="attributes",
                        to="quality_of_life.appeal",
                    ),
                ),
            ],
            options={
                "db_table": "additional_attributes",
            },
        ),
        migrations.CreateModel(
            name="ExecutionInfo",
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
                ("executors", models.TextField(db_column="executors")),
                ("executor_id", models.IntegerField(db_column="executor_id")),
                (
                    "executor_state_institute_id",
                    models.IntegerField(db_column="executor_state_institute_id"),
                ),
                ("call_status", models.IntegerField(db_column="call_status")),
                ("process_status", models.IntegerField(db_column="process_status")),
                ("current_task_id", models.IntegerField(db_column="current_task_id")),
                (
                    "appeal",
                    models.ForeignKey(
                        db_column="appeal_id",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="executions",
                        to="quality_of_life.appeal",
                    ),
                ),
            ],
            options={
                "db_table": "execution_info",
            },
        ),
        migrations.CreateModel(
            name="ResponseInfo",
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
                ("answer", models.TextField(db_column="answer")),
                ("answer_rating", models.IntegerField(db_column="answer_rating")),
                (
                    "answer_quality_id",
                    models.IntegerField(db_column="answer_quality_id"),
                ),
                (
                    "answer_rating_from_user_id",
                    models.IntegerField(db_column="answer_rating_from_user_id"),
                ),
                (
                    "appeal",
                    models.ForeignKey(
                        db_column="appeal_id",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="responses",
                        to="quality_of_life.appeal",
                    ),
                ),
            ],
            options={
                "db_table": "response_info",
            },
        ),
    ]
