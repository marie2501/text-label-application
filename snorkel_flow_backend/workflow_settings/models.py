"""
models.py

Module for defining Django models for a annotation process.


Models:
    - Workflow: A workflow represents the top unit of the annotation task.
    - File: A file represents the data set
    - Labelfunction: Represents a labelfunction associated with a workflow.
    - LabelSummary: Represents the method to summarize the labels.
    - Feature: Represents a feature extraction method.
    - Classifier: Represents a classifier that is associated with a run.
    - Run: Represents a run that belongs to a workflow and a user.
"""

from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import User


class Workflow(models.Model):
    """
    Represents a workflow.

    Attributes:
        - creator (ForeignKey): The user who created the workflow.
        - title (str): The title of the workflow.
        - creation_date (date): The date the workflow was created.
        - contributors (ManyToManyField): The users who can contribute to the workflow.
        - description (str): A description of the workflow.

    Meta:
        - unique_together (list): Ensures unique combination of title and creator.
        - ordering (list): Orders workflows by creation date in descending order.
    """

    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="workflow_creator"
    )
    title = models.CharField(max_length=200)
    creation_date = models.DateField(auto_now_add=True)
    contributors = models.ManyToManyField(User, related_name="workflow_contributors")
    description = models.TextField(null=True)

    class Meta:
        unique_together = [["title", "creator"]]
        ordering = ["-creation_date"]


def upload_to_file(instance, filename):
    """
    Generate file upload path.

    Args:
        instance (workflow_id): The ID of the workflow to which the file is linked.
        filename (str): The filename.

    Returns:
        str: The file upload path of the dataset.
    """
    return "{workflow_id}/file/{filename}".format(
        workflow_id=instance.workflow.id, filename=filename
    )


class File(models.Model):
    """
    Represents a file (dataset) associated with a workflow.

    Attributes:
        - file (FileField): The uploaded file.
        - creator (ForeignKey): The user who uploaded the file.
        - workflow (ForeignKey): The workflow the file is associated with.
    """

    file = models.FileField(upload_to=upload_to_file)
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="file_creator"
    )
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE)

    def __str__(self):
        """
        Return a string representation of the file.

        Returns:
            str: The name of the file.
        """
        return "{name}".format(name=self.file.name)


def upload_to_labelfunction(instance, filename):
    """
    Generate a labelfunction upload path.

    Args:
        instance (workflow_id): The ID of the workflow to which the file is linked.
        filename (str): The filename.

    Returns:
        str: The file upload path of the labelfunction file.
    """
    return "{workflow_id}/labelfunction/{filename}".format(
        workflow_id=instance.workflow.id, filename=filename
    )


class Labelfunction(models.Model):
    """
    Represents a labelfunction associated with a workflow.

    Attributes:
        - workflow (ForeignKey): The workflow the labelfunction is associated with.
        - creator (ForeignKey): The user who created the labelfunction.
        - type (str): The type of the labelfunction. (python_code, import, labels)
        - code (str): The code of the labelfunction.
        - name (str): The name of the labelfunction.
        - description (str): A description of the labelfunction.
        - summary_unlabeled (str): Summary (metrics) of the labelfunction performance
                                   on a unlabeled data.
        - summary_train (str): Summary (metrics) of the labelfunction performance on a
                               training data.

    Meta:
        - unique_together (list): Ensures unique combination of workflow and name.
    """

    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE)
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="labelfunction_creator"
    )
    type = models.CharField(max_length=50)
    code = models.TextField()
    name = models.CharField(max_length=150)
    description = models.TextField(null=True)
    summary_unlabeled = models.TextField(null=True)
    summary_train = models.TextField(null=True)

    class Meta:
        unique_together = [["workflow", "name"]]


class LabelSummary(models.Model):
    """
    Represents the method of summarising labels.

    Attributes:
        - type (str): The type of summary, either 'Majority Vote' or 'Probabilistic'.
    """

    choices = [("M", "Majority Vote"), ("P", "Probabilistic")]
    type = models.CharField(max_length=2, choices=choices)


class Feature(models.Model):
    """
    Represents a feature extraction method.

    Attributes:
        - type (str): The type of feature extraction, either 'Bag of Words' or 'tfidf'.
        - range_x (int): The left range of the n-gramm count.
        - range_y (int): The right range of the n-gramm count.
    """

    choices = [("BW", "Bag of Words"), ("TF", "tfidf")]
    type = models.CharField(max_length=2, choices=choices)
    range_x = models.IntegerField(validators=[MinValueValidator(1)], default=1)
    range_y = models.IntegerField(validators=[MinValueValidator(1)], default=1)


class Classifier(models.Model):
    """
    Represents a classifier.

    Attributes:
        - type (str): The type of classifier.
        - test_score (Decimal): The test score (accurancy) of the classifier.
        - train_score (Decimal): The training score (accurancy) of the classifier.
    """

    choices = [
        ("NB", "Naive Bayes"),
        ("RF", "Random Forest"),
        ("DT", "Decision Tree"),
        ("KN", "KNeighbors"),
        ("LR", "Logistic Regression"),
    ]
    type = models.CharField(max_length=2, choices=choices)
    test_score = models.DecimalField(max_digits=10, decimal_places=9)
    train_score = models.DecimalField(max_digits=10, decimal_places=9)


class Run(models.Model):
    """
    Represents a run with the associated labelfunctions.

    Attributes:
        - workflow (ForeignKey): The workflow the run is associated with.
        - creator (ForeignKey): The user who created the run.
        - labelfunctions (ManyToManyField): The labelfunctions associated with the run.
        - creation_date (date): The date the run was created.
        - labelmatrix (str): The labelmatrix of the executed run as a JSON object.
        - labelfunction_summary (str):  Summary (metrics) of the labelfunction performance
                                        on unlabeled data.
        - labelfunction_summary_train (str): Summary (metrics) of the labelfunction performance
                                             on training data.
        - preds_unlabeled (str): Predictions of the summary method for unlabeled data.
        - labelmodel (ForeignKey): The summary method for the labels associated with the run.
        - feature (ForeignKey): The feature extraction method associated with the run.
        - classifier (ForeignKey): The classifier associated with the run.

    Meta:
        ordering (list): Orders runs by creation date in descending order.
    """

    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE)
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="labelfunction_creator_run"
    )
    labelfunctions = models.ManyToManyField(Labelfunction)
    creation_date = models.DateField(auto_now_add=True)
    labelmatrix = models.TextField()
    labelfunction_summary = models.TextField(null=True)
    labelfunction_summary_train = models.TextField(null=True)
    preds_unlabeled = models.TextField(null=True)
    labelmodel = models.ForeignKey(LabelSummary, on_delete=models.CASCADE, null=True)
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE, null=True)
    classifier = models.ForeignKey(Classifier, on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ["-creation_date"]
