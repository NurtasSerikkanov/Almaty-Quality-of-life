# Generated by Django 5.1.3 on 2024-11-13 16:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        (
            "quality_of_life",
            "0006_alter_additionalattributes_budgetary_funds_are_required_and_more",
        ),
    ]

    operations = [
        migrations.RemoveField(
            model_name="appeal",
            name="index_right",
        ),
    ]
