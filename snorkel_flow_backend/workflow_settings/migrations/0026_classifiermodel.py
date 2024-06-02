# Generated by Django 3.2.20 on 2024-06-01 20:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workflow_settings', '0025_auto_20240509_1320'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClassifierModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('model', models.BinaryField()),
                ('run', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workflow_settings.run')),
            ],
        ),
    ]
