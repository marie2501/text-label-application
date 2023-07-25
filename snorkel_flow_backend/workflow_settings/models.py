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



def upload_to(instance, filename):
    print(instance, filename)
    return "{creator}/{workflow_id}/{filename}".format(creator=instance.creator.username,
                                                       workflow_id=instance.workflow.id,
                                                       filename=filename)

class File(models.Model):
    file = models.FileField(upload_to=upload_to)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='file_creator')
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE)

    def __str__(self):
        return "{creator} : {name}".format(creator=self.creator.username, name=self.file.name)



