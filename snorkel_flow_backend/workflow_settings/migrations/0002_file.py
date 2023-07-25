# Generated by Django 3.2.20 on 2023-07-25 20:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import workflow_settings.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('workflow_settings', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to=workflow_settings.models.upload_to)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='file_creator', to=settings.AUTH_USER_MODEL)),
                ('workflow', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workflow_settings.workflow')),
            ],
        ),
    ]
