"""
labelmodel_service.py

This module provides the functionalities to reduce the labels
created in a run to a single label per data point.

Classes:
- LabelModelService
"""
import json

from snorkel.labeling.model import MajorityLabelVoter, LabelModel
import numpy as np
from rest_framework import status
from workflow_settings.models import Run, LabelSummary
from workflow_settings.serializers.serializers_run import LabelModelSerializer


class LabelModelService:
    """
    Service class to reduce the labels
    created in a run to a single label per data point.

    Methods:
    - get_labelmodel_by_run_id(self, run_id):
        Retrieve the used model of a run.
    - label_model(self, run_object, selectedModelLabel, selectedTie, n_epochs=100, log_freq=10,
                  seed=123, base_learning_rate=0.01, l2=0.0, numbers_of_labels=2):
        Compute the labels.
    - __train_label_model(self, base_learning_rate, l2, log_freq, n_epochs,
                          run_object, seed, numbers_of_labels, selectedTie):
        Apply the label model to the labels
    - __majority_vote_label(self, run_object, numbers_of_labels, selectedTie):
        Apply the majority model to the labels
    """

    def get_labelmodel_by_run_id(self, run_id):
        """
        Retrieve the used model of a run.

        Args:
            run_id (int): The ID of the run.

        Returns:
            - int: A HTTP status code.
            - success: The labelmodel object.
            - error: A dict with an error message
        """
        run_filter = Run.objects.filter(pk=run_id)
        if run_filter.exists():
            run_object = run_filter[0]
            labelmodel_serializer = LabelModelSerializer(data=run_object.labelmodel)
            return status.HTTP_200_OK, labelmodel_serializer.data
        return status.HTTP_404_NOT_FOUND, {"message": "Run object doesn't exists"}

    def label_model(
        self,
        run_object,
        selected_model_label,
        selected_tie,
        n_epochs=100,
        log_freq=10,
        seed=123,
        base_learning_rate=0.01,
        l2=0.0,
        numbers_of_labels=2,
    ):
        """
        Compute the labels. The choosen labelmodel of the user gets applied on the run.

        Args:
            run_object (Run): The Run object.
            selected_model_label (str): The labelmodel to be applied ("Majority Vote" or "Train Label Model").
            selected_tie (str): The tie-breaking policy.
            n_epochs (int, optional): Number of epochs for training. Defaults to 100.
            log_freq (int, optional): The log frequency. Defaults to 10.
            seed (int, optional): Random seed. Defaults to 123.
            base_learning_rate (float, optional): Base learning rate. Defaults to 0.01.
            l2 (float, optional): L2 regularization parameter. Defaults to 0.0.
            numbers_of_labels (int, optional): Number of labels. Defaults to 2.


        Returns:
            ndarray: A ndarray with the labelmodel predictions or an error message.
        """
        if selected_model_label == "Majority Vote":
            label = LabelSummary.objects.get_or_create(type="M")
            run_object.labelmodel = label[0]
            run_object.save()
            return self.__majority_vote_label(
                run_object, numbers_of_labels, selected_tie
            )
        elif selected_model_label == "Train Label Model":
            label = LabelSummary.objects.get_or_create(type="P")
            run_object.labelmodel = label[0]
            run_object.save()
            return self.__train_label_model(
                base_learning_rate,
                l2,
                log_freq,
                n_epochs,
                run_object,
                seed,
                numbers_of_labels,
                selected_tie,
            )
        return {"message": "Choose a valid label service"}

    def __train_label_model(
        self,
        base_learning_rate,
        l2,
        log_freq,
        n_epochs,
        run_object,
        seed,
        numbers_of_labels,
        selectedTie,
    ):
        """
        Trains a labelmodel and predicts labels for the given run.

        Args:
           base_learning_rate (float): Base learning rate.
           l2 (float): L2 regularization parameter.
           log_freq (int): The log frequency.
           n_epochs (int): Number of epochs for training.
           run_object (Run): The Run object.
           seed (int): Random seed.
           numbers_of_labels (int): Number of labels.
           selectedTie (str): The tie-breaking policy.

        Returns:
           ndarray: Predicted labels for the unlabeled data.
        """
        label_model = LabelModel(cardinality=numbers_of_labels, verbose=True)
        labelmatrix_json = json.loads(run_object.labelmatrix)
        labelmatrix = np.array(labelmatrix_json)
        label_model.fit(
            L_train=labelmatrix,
            n_epochs=n_epochs,
            log_freq=log_freq,
            seed=seed,
            lr=base_learning_rate,
            l2=l2,
        )
        preds_unlabeled = label_model.predict(
            L=labelmatrix, tie_break_policy=selectedTie
        )
        return preds_unlabeled

    def __majority_vote_label(self, run_object, numbers_of_labels, selectedTie):
        """
        Applies majority vote labeling to the given run.

        Args:
            run_object (Run): The Run object.
            numbers_of_labels (int): Number of labels.
            selectedTie (str): The tie-breaking policy.

        Returns:
            ndarray: Predicted labels for the unlabeled data.
        """
        majority_model = MajorityLabelVoter(cardinality=numbers_of_labels)
        labelmatrix_json = json.loads(run_object.labelmatrix)
        labelmatrix = np.array(labelmatrix_json)
        preds_unlabeled = majority_model.predict(
            L=labelmatrix, tie_break_policy=selectedTie
        )
        return preds_unlabeled
