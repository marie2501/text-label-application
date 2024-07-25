# Generated by Django 3.2.20 on 2024-07-25 21:56

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import workflow_settings.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Classifier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('NB', 'Naive Bayes'), ('RF', 'Random Forest'), ('DT', 'Decision Tree'), ('KN', 'KNeighbors'), ('LR', 'Logistic Regression')], max_length=2)),
                ('test_score', models.DecimalField(decimal_places=9, max_digits=10)),
                ('train_score', models.DecimalField(decimal_places=9, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('BW', 'Bag of Words'), ('TF', 'tfidf')], max_length=2)),
                ('range_x', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ('range_y', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
            ],
        ),
        migrations.CreateModel(
            name='Labelfunction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=50)),
                ('code', models.TextField()),
                ('name', models.CharField(max_length=150)),
                ('description', models.TextField(null=True)),
                ('summary_unlabeled', models.TextField(null=True)),
                ('summary_train', models.TextField(null=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='labelfunction_creator', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LabelSummary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('M', 'Majority Vote'), ('P', 'Probabilistic')], max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Workflow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('creation_date', models.DateField(auto_now_add=True)),
                ('description', models.TextField(null=True)),
                ('contributors', models.ManyToManyField(related_name='workflow_contributors', to=settings.AUTH_USER_MODEL)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='workflow_creator', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-creation_date'],
                'unique_together': {('title', 'creator')},
            },
        ),
        migrations.CreateModel(
            name='Run',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateField(auto_now_add=True)),
                ('labelmatrix', models.TextField()),
                ('labelfunction_summary', models.TextField(null=True)),
                ('labelfunction_summary_train', models.TextField(null=True)),
                ('preds_unlabeled', models.TextField(null=True)),
                ('classifier', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='workflow_settings.classifier')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='labelfunction_creator_run', to=settings.AUTH_USER_MODEL)),
                ('feature', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='workflow_settings.feature')),
                ('labelfunctions', models.ManyToManyField(to='workflow_settings.Labelfunction')),
                ('labelmodel', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='workflow_settings.labelsummary')),
                ('workflow', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workflow_settings.workflow')),
            ],
            options={
                'ordering': ['-creation_date'],
            },
        ),
        migrations.AddField(
            model_name='labelfunction',
            name='workflow',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workflow_settings.workflow'),
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to=workflow_settings.models.upload_to_file)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='file_creator', to=settings.AUTH_USER_MODEL)),
                ('workflow', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workflow_settings.workflow')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='labelfunction',
            unique_together={('workflow', 'name')},
        ),
    ]
