# Generated by Django 3.2.20 on 2024-04-26 17:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workflow_settings', '0020_run_preds_unlabeled'),
    ]

    operations = [
        migrations.RenameField(
            model_name='run',
            old_name='labelsummary',
            new_name='labelmodel',
        ),
    ]
