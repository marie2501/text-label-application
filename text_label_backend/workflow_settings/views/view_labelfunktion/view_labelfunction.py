"""
Module for creating, managing and modifying labelfunctions in a workflow.

This module defines the views for managing labelfunctions, including
creating, updating, retrieving, and deleting labelfunctions within
a specified workflow. The views interact with the LabelfunctionService
to perform the necessary operations and handle the responses.

Classes:
    - LabelfunctionView: ViewSet for managing labelfunctions, imports an labels in a workflow.
    - LabelfunctionModifyView: ViewSet for modifying existing labelfunctions.
"""

from rest_framework import status, authentication, viewsets
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from workflow_settings.permissions import (
    IsLabelfuntionCreatorPermission,
    WorkflowAccessPermission,
)
from workflow_settings.serializers.serializers_labelfunction import (
    LabelfunctionCreateSerializer,
)
from workflow_settings.services.labelfunktion_service.labelfunction_service import (
    LabelfunctionService,
)


class LabelfunctionView(viewsets.ViewSet):
    """
    ViewSet for creating and managing labelfunctions, imports and labels in a workflow.

    Provides methods to get and update the imports and the required labels, to
    get all label functions by workflow ID, and to create a new labelfunction.

    Authentication Classes:
        - TokenAuthentication

    Permission Classes:
        - IsAuthenticated
        - WorkflowAccessPermission

    Parser Classes:
        - JSONParser
    """

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated, WorkflowAccessPermission]
    parser_class = [JSONParser]

    def get_import_labels(self, request, *args, **kwargs):
        """
        Retrieve import statments or the label definition for a given workflow.
        The type determines which object is returned

        Path Parameters:
            - workflow_id (int): The ID of the workflow.
            - type (str): The type of the labelfunction to retrieve.

        Returns:
            - Response: Contains the status and data (from type labelfunction).

        Errors:
            - Response: Contains a 404 status and a error message {meassage: string}.
        """
        workflow_id = kwargs["workflow_id"]
        type_labelfunction = kwargs["type"]

        labelfunction = LabelfunctionService()
        status_code, data = labelfunction.get_import_labels(workflow_id, type_labelfunction)

        return Response(status=status_code, data=data)

    def update_import_labels(self, request, *args, **kwargs):
        """
        update import statments or the label definition for a given workflow.
        The type determines which object is returned

        Path Parameters:
            - workflow_id (int): The ID of the workflow.

        Request Data:
            - type (str): The type of the labelfunction to update.
            - labelfunction object that is to be updated

        Returns:
            - Response: A response containing the status and a success message.

        Errors:
            - Response: A response containing the status and a error message.
        """
        workflow_id = kwargs["workflow_id"]
        request_data = request.data
        type_labelfunction = request.data["type"]

        labelfunction = LabelfunctionService()
        status_code, data = labelfunction.update_import_labels(
            workflow_id, request_data, type_labelfunction
        )
        return Response(status=status_code, data=data)

    def get_all_labelfunction_by_workflow_id(self, request, *args, **kwargs):
        """
        Retrieve all labelfunctions for a given workflow.

        Path Parameters:
            - workflow_id (int): The ID of the workflow.

        Returns:
            - Response: A response containing the status and a list of labelfunction objects.
        """
        workflow_id = kwargs["workflow_id"]

        labelfunction = LabelfunctionService()
        status_code, data = labelfunction.get_all_labelfunction_by_workflow_id(workflow_id)
        return Response(status=status_code, data=data)

    def add_labelfunction(self, request, *args, **kwargs):
        """
        Add a new labelfunction to a workflow. The labelfunction gets compiled,
        tested on the dataset and created.

        Path Parameters:
            - workflow_id (int): The ID of the workflow.

        Request Data:
            - request.data: labelfunction obejct.
                - code (str): The code of the labelfunction.
                - name (str): The name of the labelfunction.

        Returns:
            - Response: A response containing the status and the data of the operations.
                        {summary: AnalysisModel, summary_train: AnalysisModel,
                         df_combined: DataframeModel[], lid: number}

         Errors:
             - Response: A response containing the status and a error message.
        """
        workflow_id = kwargs["workflow_id"]
        request_data = request.data
        request_data["workflow"] = workflow_id
        labelfunction_code = request.data["code"]
        name = request.data["name"]

        labelfunction = LabelfunctionService()

        # First step: Compile Pythoncode
        status_compile, data_c = labelfunction.compile_labelfunction(
            workflow_id, labelfunction_code
        )
        if status_compile == status.HTTP_200_OK:
            # Second step: Test Pythoncode on real Dataset
            status_test, data_t = labelfunction.test_labelfunction(
                workflow_id, labelfunction_code, name
            )
            # Third step: Save Function
            if status_test == status.HTTP_200_OK:
                request_data["summary_unlabeled"] = data_t["summary"].to_json(
                    orient="split"
                )
                request_data["summary_train"] = data_t["summary_train"].to_json(
                    orient="split"
                )
                serialziers_label = LabelfunctionCreateSerializer(data=request_data)
                status_save, data_s = labelfunction.add_labelfunction(
                    request.user, serialziers_label
                )
                if status_save == status.HTTP_201_CREATED:
                    data_s.update(data_t)
                return Response(status=status_save, data=data_s)
            return Response(status=status_test, data=data_t)
        return Response(status=status_compile, data=data_c)


class LabelfunctionModifyView(viewsets.ViewSet):
    """
    ViewSet to change and delete the labelfunctions.

    Provides methods to get, delete, and update a labelfunction by its ID.

    Authentication Classes:
        - TokenAuthentication

    Permission Classes:
        - IsAuthenticated
        - IsLabelfuntionCreatorPermission

    Parser Classes:
        - JSONParser
    """

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated, IsLabelfuntionCreatorPermission]
    parser_class = [JSONParser]

    def get_labelfunction_by_id(self, request, *args, **kwargs):
        """
        Retrieve a labelfunction by its ID.

        Path Parameters:
            - labelfunction_id (int): The ID of the label function.

        Returns:
            - Response: A response containing the status and  the labelfunction object.

        Errors:
            - Response: A response containing the status and a error message.
        """
        labelfunction_id = kwargs["labelfunction_id"]

        labelfunction = LabelfunctionService()
        status_code, data = labelfunction.get_labelfunction_by_id(labelfunction_id)

        return Response(status=status_code, data=data)

    def delete_labelfunction(self, request, *args, **kwargs):
        """
        Delete a labelfunction by its ID.

        Requirement:
        The label function must not be used in any run.

        Path Parameters:
            - labelfunction_id (int): The ID of the label function.

        Returns:
            - Response: A response containing the status and a success message.

        Errors:
            - Response: A response containing the status and a error message.
        """
        labelfunction_id = kwargs["labelfunction_id"]

        labelfunction = LabelfunctionService()
        status_code, data = labelfunction.delete_labelfunction(labelfunction_id)
        return Response(status=status_code, data=data)

    def update_labelfunction(self, request, *args, **kwargs):
        """
        Update a labelfunction by its ID. The labelfunction gets compiled,
        tested on the dataset and updated.

        Path Parameters:
            - labelfunction_id (int): The ID of the labelfunction.

        Request Data:
            - workflow_id (int): The ID of the workflow.
            - labelfunction (dict): The label function data including code and name.

        Returns:
            - Response: A response containing the status and the data of the operations.
                        {summary: AnalysisModel, summary_train: AnalysisModel,
                         df_combined: DataframeModel[], lid: number}

         Errors:
             - Response: A response containing the status and a error message.
        """
        labelfunction_id = kwargs["labelfunction_id"]
        request_data = request.data
        workflow_id = request_data["workflow_id"]
        labelfunction_obj = request_data["labelfunction"]

        labelfunction_service = LabelfunctionService()

        status_compile, data_c = labelfunction_service.compile_labelfunction(
            workflow_id, labelfunction_obj["code"]
        )
        if status_compile == status.HTTP_200_OK:
            # Second step: Test Pythoncode on real Dataset
            status_test, data_t = labelfunction_service.test_labelfunction(
                workflow_id, labelfunction_obj["code"], labelfunction_obj["name"]
            )
            # Third step: Save Function
            if status_test == status.HTTP_200_OK:
                labelfunction_obj["summary_unlabeled"] = data_t["summary"].to_json(
                    orient="split"
                )
                labelfunction_obj["summary_train"] = data_t["summary_train"].to_json(
                    orient="split"
                )
                status_save, data_s = labelfunction_service.update_labelfunction(
                    labelfunction_id, labelfunction_obj
                )
                if status_save == status.HTTP_200_OK:
                    data_s.update(data_t)
                return Response(status=status_save, data=data_s)
            return Response(status=status_test, data=data_t)
        return Response(status=status_compile, data=data_c)
