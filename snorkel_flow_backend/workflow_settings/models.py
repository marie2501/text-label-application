from django.core.exceptions import NON_FIELD_ERRORS
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
    contributors = models.ManyToManyField(User, related_name='workflow_contributors', default=creator)
    # Prozentzahl - Anteil der Datenpunkte für das Testdatenset
    splitting_ratio_labeled_test = models.DecimalField(max_digits=4, decimal_places=2, default=50.00)

    class Meta:
        unique_together = [["title", "creator"]]
        ordering = ["-creation_date"]



def upload_to_file(instance, filename):
    return "{workflow_id}/file/{creator}/{filename}".format(creator=instance.creator.username,
                                                       workflow_id=instance.workflow.id,
                                                       filename=filename)

class File(models.Model):
    file = models.FileField(upload_to=upload_to_file)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='file_creator')
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE)

    def __str__(self):
        return "{name}".format(name=self.file.name)

# todo löschen, als file richtig speichern und mit pandas file immer einlesen
# class Datapoint(models.Model):
#     Development = "D"
#     Test = "T"
#     Unlabeled = "U"
#
#     Stages = [
#         (Development, "Development"),
#         (Test, "Test"),
#         (Unlabeled, "Unlabeled"),
#     ]
#
#     corpus_id = models.IntegerField()
#     tweet_id = models.CharField(max_length=30)
#     text = models.CharField(max_length=400)
#     splitting = models.CharField(
#         max_length=1,
#         choices=Stages,
#         default=Unlabeled,
#     )
#     workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE)

def get_default_user():
    return User.objects.get_or_create(username="default")[0]


# def count_function_by_workflow(workflow_id):
#     return Workflow.objects.filter(pk=workflow_id).count()

def upload_to_labelfunction(instance, filename):
    return "{workflow_id}/labelfunction/{filename}".format(workflow_id=instance.workflow.id,
                                                                   filename=filename)

class Labelfunctions(models.Model):
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE)
    file = models.FileField(upload_to=upload_to_labelfunction)

