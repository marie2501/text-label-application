# Generated by Django 3.2.20 on 2024-05-08 00:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workflow_settings', '0022_alter_classifier_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workflow',
            name='is_public',
        ),
    ]
