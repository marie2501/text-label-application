from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Workflow(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workflow_creator')
    title = models.CharField(max_length=200)
    creation_date = models.DateField(auto_now_add=True)
    # is_public : True -> alle können Workflow einsehen
    # is_public : False -> nur Creator und Contibutors können Workflow einsehen
    is_public = models.BooleanField()
    # contributer : dürfen alles außer Workflow löschen
    contributors = models.ManyToManyField(User, related_name='workflow_contributors')
    # todo implementiern bei frontend und backend
    description = models.TextField(null=True)

    class Meta:
        unique_together = [["title", "creator"]]
        ordering = ["-creation_date"]

def upload_to_file(instance, filename):
    return "{workflow_id}/file/{filename}".format(workflow_id=instance.workflow.id, filename=filename)

class File(models.Model):
    file = models.FileField(upload_to=upload_to_file)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='file_creator')
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE)

    def __str__(self):
        return "{name}".format(name=self.file.name)

def upload_to_labelfunction(instance, filename):
    return "{workflow_id}/labelfunction/{filename}".format(workflow_id=instance.workflow.id, filename=filename)

# Speichert die Labelfunktionen in der Datenbank
class Labelfunction(models.Model):
    # todo falls labelfunction in einem workflow ist -> nicht vollständig löschen
    #  sondern nur workflow und creator reference/oder verhindern
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='labelfunction_creator')
    type = models.CharField(max_length=50)
    code = models.TextField()
    name = models.CharField(max_length=150)

    class Meta:
        unique_together = [["workflow", "name"]]

class LabelSummary(models.Model):
    # speichere die zusammenfassung der Labelmatrix -> jeder datenpunkt bildet nur noch auf ein label ab
    choices = [('M', 'Majority Vote'), ('P', 'Probabilistic')]
    type = models.CharField(max_length=2, choices=choices)

class Feature(models.Model):
    choices = [('BW', 'Bag of Words'), ('TF', 'tfidf')]
    type = models.CharField(max_length=2, choices=choices)
    range_x = models.IntegerField(validators=[MinValueValidator(1)], default=1)
    range_y = models.IntegerField(validators=[MinValueValidator(1)], default=1)

class Classifier(models.Model):
    choices = [('NB', 'Naive Bayes')]
    type = models.CharField(max_length=2, choices=choices)
    test_score = models.DecimalField(max_digits=10, decimal_places=9)
    train_score = models.DecimalField(max_digits=10, decimal_places=9)

# Speichert die Labelfunktionen der verschiedenen Runs
class Run(models.Model):
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='labelfunction_creator_run')
    labelfunctions = models.ManyToManyField(Labelfunction)
    creation_date = models.DateField(auto_now_add=True)
    # speichere Labelmatrix als json object
    labelmatrix = models.TextField()
    labelfunction_summary = models.TextField(null=True)
    labelfunction_summary_train = models.TextField(null=True)
    preds_unlabeled = models.TextField(null=True)
    labelmodel = models.ForeignKey(LabelSummary, on_delete=models.CASCADE, null=True)
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE, null=True)
    classifier = models.ForeignKey(Classifier, on_delete=models.CASCADE, null=True)


    class Meta:
        ordering = ["-creation_date"]



