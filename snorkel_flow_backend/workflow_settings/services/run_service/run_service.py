"""
run_service.py

The module provides a service that enables the management of Run objects.

Classes:
- RunService
"""

import json
import sys

import numpy as np
from snorkel.labeling import PandasLFApplier, LFAnalysis
import pandas as pd
from zen_queries import fetch, queries_disabled


from rest_framework import status

from snorkel_flow_backend.settings import MEDIA_ROOT
from workflow_settings.models import Labelfunction, Run, File
from workflow_settings.serializers.serializers_run import (
    RunCreateSerializer,
    RunSerializer,
)


class RunService:
    """
    A service for the management of Run objects.

    Methods:
        - get_access(self, run_id, request_user):
            Checks whether a user is authorised to access a run.
        - exec_run(self, run_id):
            Executes all labelfunctions associated with a specific run.
        - __execute_run_on_dataset( self, file_path, imports, run_labelfunctions,
                                    run_obeject, labels_code=""):
            Executes all labelfunctions associated with a specific run.
        - get_run(self, run_id):
            Retrieves a Run by its ID.
        - list_run(self, workflow_id, request_user):
            Retrieves all Runs of a user of a workflow.
        - create_run(self, workflow_id, run_serializer, request_user):
            Creates a new Run.
        - update_run(self, run_id, request_data):
            Updates a Run.
    """

    def get_access(self, run_id, request_user):
        """
        Checks whether a user is authorised to access a run.

        Args:
            run_id (int): The ID of the run.
            request_user (User): The user who wants to access the run.

        Returns:
            - int: A HTTP status code.
            - bool: True if the user gets access, otherwise False
        """
        run_filter = Run.objects.filter(pk=run_id, creator=request_user)
        if run_filter.exists():
            return status.HTTP_200_OK, True
        return status.HTTP_200_OK, False

    def exec_run(self, run_id):
        """
        Executes all labelfunctions associated with a specific run.

        Args:
            run_id (int): The ID of the run.

        Returns:
            - int: A HTTP status code.
            - data (dict): The metrics of the labelfunctions on the unlabeled and train dataset
            - L_train_train (ndarray): Label predictions of the train dataset.
            - dataframe_train (Dataframe): Train dataset.
            - labelfunction_names (list): list of the labelfunctionnames of a run
            - error: A dict with an error message.
        """
        run_filter = Run.objects.filter(pk=run_id)
        if run_filter.exists():
            run_obeject = run_filter[0]
            run_labelfunctions = run_obeject.labelfunctions.all()
            workflow_id = run_filter[0].workflow_id
            file = File.objects.filter(workflow_id=workflow_id)
            if file.exists():
                file_name = file[0].__str__()
                file_path = "{root}/{name}".format(root=MEDIA_ROOT, name=file_name)
                imports = Labelfunction.objects.filter(
                    workflow_id=run_filter[0].workflow_id, type="import"
                )
                if imports.exists():
                    labels = Labelfunction.objects.filter(
                        workflow_id=workflow_id, type="labels"
                    )
                    if labels.exists():
                        labels_code = labels[0].code
                        return self.__execute_run_on_dataset(
                            file_path,
                            imports,
                            run_labelfunctions,
                            run_obeject,
                            labels_code,
                        )
                    return self.__execute_run_on_dataset(
                        file_path, imports, run_labelfunctions, run_obeject
                    )
        return status.HTTP_404_NOT_FOUND, {"message": "The run does not exist"}

    def __execute_run_on_dataset(
        self, file_path, imports, run_labelfunctions, run_obeject, labels_code=""
    ):
        """
        Executes all labelfunctions associated with a specific run.

        Args:
            file_path (str): The path to the dataset CSV file.
            imports (QuerySet): A QuerySet containing the import statements for the run.
            run_labelfunctions (QuerySet): A QuerySet containing the labelfunctions to be executed.
            run_obeject (Run): The Run object associated with the current execution.
            labels_code (str): The code defining the labels. Defaults to ''.


        Returns:
            - int: A HTTP status code.
            - data (dict): The metrics of the labelfunctions on the unlabeled and train dataset
            - l_train_train (ndarray): Label predictions of the train dataset.
            - dataframe_train (Dataframe): Train dataset.
            - labelfunction_names (list): list of the labelfunctionnames of a run
            - error: A dict with an error message.
        """
        try:
            exec(imports[0].code, locals())
            exec(labels_code, locals())
            dataframe = pd.read_csv(file_path)

            dataframe_unlabeled = dataframe.loc[
                (dataframe["splitting_id"] == "unlabeled")
            ]
            dataframe_train = dataframe.loc[(dataframe["splitting_id"] == "train")]
            text_list_train_gold_labels = np.array(dataframe_train["CLASS"].tolist())

            labelfunction_names = []
            for item in run_labelfunctions:
                exec(item.code, locals())
                labelfunction_names.append(item.name)
            local_vars = locals()

            labelfunction_reference = []
            for label in labelfunction_names:
                labelfunction_reference.append(local_vars[label])

            with queries_disabled():
                applier = PandasLFApplier(lfs=labelfunction_reference)
                l_train_unlabeled = applier.apply(df=dataframe_unlabeled)
                l_train_train = applier.apply(df=dataframe_train)

            summary = LFAnalysis(
                L=l_train_unlabeled, lfs=labelfunction_reference
            ).lf_summary()
            summary_train = LFAnalysis(
                L=l_train_train, lfs=labelfunction_reference
            ).lf_summary(Y=text_list_train_gold_labels)
            summary["index"] = summary.index
            summary_train = summary_train.rename(columns={"Emp. Acc.": "EmpAcc"})
            summary_train["index"] = summary_train.index

            data = {"summary": summary, "summary_train": summary_train}
            labelmatrix = json.dumps(l_train_unlabeled.tolist())
            run_obeject.labelfunction_summary = summary.to_json(orient="split")
            run_obeject.labelmatrix = labelmatrix
            run_obeject.labelfunction_summary_train = summary_train.to_json(
                orient="split"
            )
            run_obeject.save()
            return (
                status.HTTP_200_OK,
                data,
                l_train_train,
                dataframe_train,
                labelfunction_names,
            )
        except:
            data = str(sys.exc_info())
            return status.HTTP_400_BAD_REQUEST, data

    def get_run(self, run_id):
        """
        Retrieves a Run by its ID.

        Args:
            run_id (int): The ID of the run.

        Returns:
            - int: A HTTP status code.
            - dict: The run objects or a error message.
        """
        run = Run.objects.filter(pk=run_id)
        if run.exists():
            run_obj = run[0]
            run_serializer = RunSerializer(run_obj)
            return status.HTTP_200_OK, run_serializer.data
        return status.HTTP_404_NOT_FOUND, {"message": "The run object does not exist"}

    def list_run(self, workflow_id, request_user):
        """
        Retrieves all Runs of a user of a workflow.

        Args:
            workflow_id (int): The ID of the workflow.
            request_user (User): The request user who wants to access the runs.

        Returns:
            - int: A HTTP status code.
            - list: A list of run objects.
        """
        labelfunction_run = Run.objects.filter(
            workflow_id=workflow_id, creator=request_user
        )
        if labelfunction_run.exists():
            run_serializer = RunSerializer(labelfunction_run, many=True)
            return status.HTTP_200_OK, run_serializer.data
        return status.HTTP_200_OK, []

    def create_run(self, workflow_id, run_serializer, request_user):
        """
        Creates a new Run.

        Args:
            workflow_id (int): The ID of the workflow.
            request_user (User): The request user who creates the runs.
            run_serializer (Serializer): The serializes run object.

        Returns:
            - int: A HTTP status code.
            - dict: Returns a success or error message.
        """
        if run_serializer.is_valid():
            print(run_serializer)
            run_serializer.save(creator=request_user, workflow_id=workflow_id)
            return status.HTTP_201_CREATED, {"message": "Run was successfuly created"}
        return status.HTTP_400_BAD_REQUEST, run_serializer.errors

    def update_run(self, run_id, request_data):
        """
        Updates a Run.

        Args:
            run_id (int): The ID of the run.
            request_data (dict): The data contains the run object which will be updated.

        Returns:
            - int: A HTTP status code.
            - dict: Returns a success or error message.
        """
        run_obj = Run.objects.filter(pk=run_id)
        if run_obj.exists():
            run = run_obj[0]
            run_serializer = RunCreateSerializer(run, data=request_data, partial=True)
            if run_serializer.is_valid():
                run_serializer.save()
                return status.HTTP_201_CREATED, {
                    "message": "Run was successfuly created"
                }
            return status.HTTP_400_BAD_REQUEST, run_serializer.errors
        return status.HTTP_404_NOT_FOUND, {"message": "The run object does not exist"}
