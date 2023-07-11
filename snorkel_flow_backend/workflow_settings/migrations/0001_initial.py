# Generated by Django 3.2.20 on 2023-07-11 23:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Workflow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('creation_date', models.DateField(auto_now_add=True)),
                ('is_public', models.BooleanField()),
                ('contributors', models.ManyToManyField(related_name='workflow_contributors', to=settings.AUTH_USER_MODEL)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='workflow_creator', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
