# Generated by Django 3.2.20 on 2023-11-05 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workflow_settings', '0010_remove_run_splitting_ratio_labeled_test'),
    ]

    operations = [
        migrations.AddField(
            model_name='run',
            name='labelfunction_reference',
            field=models.TextField(null=True),
        ),
    ]
