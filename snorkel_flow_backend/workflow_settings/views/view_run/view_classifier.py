"""
view_classifier.py

Module for handling classifier operations in a workflow run.

This module provides a Django REST framework ViewSet for executing classifiers on
workflow runs. It provides functions for creating individual labels and
features and for training a classifier.

Classes:
    - ClassiferView: A ViewSet for handling classifier operations.
"""

import pandas as pd
from rest_framework import authentication, viewsets
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from workflow_settings.permissions import IsRunCreatorPermission
from workflow_settings.services.run_service.classifier_service import ClassiferService
from workflow_settings.services.run_service.run_service import RunService


class ClassiferView(viewsets.ViewSet):
    """
    ViewSet for creating individual labels and features
    and for training a classifier.

    Authentication Classes:
    - TokenAuthentication

    Permission Classes:
    - IsAuthenticated
    - IsRunCreatorPermission

    Parser Classes:
    - JSONParser
    """

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated, IsRunCreatorPermission]
    parser_class = [JSONParser]

    # todo get number of labels automatisch wichtig

    def call_classifier(self, request, *args, **kwargs):
        """
        For a given run.
        Executes the operation needed for training a classifier,
        and trains the requestet classifier.

        Path Parameters:
            - run_id (int): The ID of the workflow run.

        Request Data:
            - selectedModelClassifier (str): The selected model for classification.
            - selectedModelLabel (str): The selected model for summarising labels.
            - selectedModelFeaturize (str): The selected model for featurization.
            - range_x (int): The range X value for featurization regarding ngramm. (optional)
            - range_y (int): The range Y value for featurization regarding ngramm. (optional)
            - n_epochs (int): The number of epochs for training. (optional)
            - log_freq (int): The logging frequency during training. (optional)
            - seed (int): The seed value for random number generation. (optional)
            - base_learning_rate (float): The base learning rate for the model. (optional)
            - l2 (float): The L2 regularization value. (optional)
            - selectedTie (bool): Whether to use for tie-breaking a specific
                                  policy for summarising labels.
            - filterAbstain (bool): Whether to filter abstained in the summarising
                                    labels before a clssifier is traines.

        Returns:
            Response: HTTP response containing score for train, test and a datarfame
                      of labelpredictions for the test set

        Errors:
            - Response: A response containing the status and a error message.
        """
        run_id = kwargs["run_id"]
        selected_model_classifier = request.data["selectedModelClassifier"]
        selected_model_label = request.data["selectedModelLabel"]
        selected_model_featurize = request.data["selectedModelFeaturize"]
        range_x = request.data["range_x"]
        range_y = request.data["range_y"]
        n_epochs = request.data["n_epochs"]
        log_freq = request.data["log_freq"]
        seed = request.data["seed"]
        base_learning_rate = request.data["base_learning_rate"]
        l2 = request.data["l2"]
        selected_tie = request.data["selectedTie"]
        filter_abstain = request.data["filterAbstain"]
        # todo get automatically
        numbers_of_labels = 2

        runservice = RunService()
        status, data, l_train_train, dataframe_train, labelfunction_names = (
            runservice.exec_run(run_id)
        )

        classifierservice = ClassiferService()
        status, data, predictions_train = classifierservice.call_classifier(
            run_id,
            selected_model_classifier,
            selected_model_label,
            selected_model_featurize,
            range_x,
            range_y,
            n_epochs,
            log_freq,
            seed,
            base_learning_rate,
            l2,
            numbers_of_labels,
            selected_tie,
            filter_abstain,
        )

        labelfunctions_dataframe = pd.DataFrame(
            l_train_train, columns=labelfunction_names
        )
        if labelfunctions_dataframe.shape[0] == dataframe_train.shape[0]:
            labelfunctions_dataframe = labelfunctions_dataframe.reset_index(drop=True)
            dataframe_train = dataframe_train[
                ["entity_id", "corpus_id", "text", "splitting_id", "CLASS"]
            ]
            dataframe_train = dataframe_train.reset_index(drop=True)
            df_combined = pd.concat([dataframe_train, labelfunctions_dataframe], axis=1)
            df_combined["Classifier_predictions"] = predictions_train
            df_combined = df_combined.fillna("")

            json_dataframe = df_combined.to_dict(orient="split")
            data.update({"df_combined": json_dataframe})

            return Response(data=data, status=status)

        return Response(data=data, status=status)
