# Generated by Django 3.2.20 on 2023-11-19 22:43

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workflow_settings', '0013_auto_20231119_2240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feature',
            name='range_x',
            field=models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='feature',
            name='range_y',
            field=models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]
