"""
view_run.py

Module for managing runs in a workflow through Django REST framework ViewSets.

This module provides ViewSets for authenticating access, executing runs,
retrieving individual runs, updating runs, creating new runs and
listing runs.

Classes:
    - RunAuthenticateView: A ViewSet for authenticating access to runs.
    - RunView: A ViewSet for executing, retrieving, and updating runs.
    - RunCreateView: A ViewSet for creating and listing runs.
"""

from rest_framework import authentication, viewsets
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from workflow_settings.permissions import (
    WorkflowAccessPermission,
    IsRunCreatorPermission,
)
from workflow_settings.serializers.serializers_run import RunCreateSerializer
from workflow_settings.services.run_service.run_service import RunService


class RunAuthenticateView(viewsets.ViewSet):
    """
    ViewSet for authenticating access to runs.

    Authentication Classes:
        - TokenAuthentication

    Permission Classes:
        - IsAuthenticated

    Parser Classes:
        - JSONParser
    """

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated]
    parser_class = [JSONParser]

    def get_access(self, request, *args, **kwargs):
        """
        Authenticate access to a run.

        Path Parameters:
            - run_id (int): The ID of the run.

        Returns:
            - Response: A HTTP response containing the status and a boolean.
        """
        run_id = kwargs["run_id"]

        runservice = RunService()
        status, data = runservice.get_access(run_id, request.user)

        return Response(data=data, status=status)


class RunView(viewsets.ViewSet):
    """
    ViewSet for executing, retrieving, and updating runs.

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

    def exec_run(self, request, *args, **kwargs):
        """
        Execute a run by its ID.

        Path Parameters:
            - run_id (int): The ID of the run.

        Returns:
            - Response: The HTTP response containing the status and
                        {'summary': AnalysisModel, 'summary_train': AnalysisModel}.
                        The AnalysisModel ist a pd dataframe with the values of the computed metrics
                        (Coverage, Conflicts, Polarity, Overlaps, Correct, Incorrect, EmpAcc, index

        Errors:
            - Response: A HTTP response containing the status and a error message.
        """
        run_id = kwargs["run_id"]

        runservice = RunService()
        status, data, l_train_train, dataframe_train, labelfunction_names = (
            runservice.exec_run(run_id)
        )

        return Response(status=status, data=data)

    def get_run_by_id(self, request, *args, **kwargs):
        """
        Retrieve a run by its ID.

        Path Parameters:
            - run_id (int): The ID of the run.

        Returns:
            Response: The HTTP response containing the status and the run object.

        Errors:
            - Response: A HTTP response containing the status and a error message.
        """
        run_id = kwargs["run_id"]

        runservice = RunService()
        status, data = runservice.get_run(run_id)

        return Response(status=status, data=data)

    def update_run(self, request, *args, **kwargs):
        """
        Update a run by its ID.

        Path Parameters:
            - run_id (int): The ID of the run.

         Returns:
             - Response: The HTTP response containing the status and a success message.

         Errors:
             - Response: A HTTP response containing the status and a error message.
        """
        run_id = kwargs["run_id"]

        runservice = RunService()
        status, data = runservice.update_run(run_id, request.data)

        return Response(status=status, data=data)


class RunCreateView(viewsets.ViewSet):
    """
    ViewSet for creating and listing runs.

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

    def create_run(self, request, *args, **kwargs):
        """
        Create a new run in a workflow.

        Path Parameters:
            - workflow_id (int): The ID of the workflow.

        Returns:
            - Response: The HTTP response containing the status and a success message.

        Errors:
            - Response: A HTTP response containing the status and a error message.
        """
        workflow_id = kwargs["workflow_id"]
        print(request.data)

        run_serializer = RunCreateSerializer(data=request.data)

        runservice = RunService()
        status, data = runservice.create_run(workflow_id, run_serializer, request.user)

        print(status)
        print(data)

        return Response(status=status, data=data)

    def list_run(self, request, *args, **kwargs):
        """
        List all runs of the request user in a workflow.

        Path Parameters:
            - workflow_id (int): The ID of the workflow.

        Returns:
            - Response: The HTTP response containing the status and a list of run objects.
        """
        workflow_id = kwargs["workflow_id"]

        runservice = RunService()
        status, data = runservice.list_run(workflow_id, request.user)

        return Response(status=status, data=data)
