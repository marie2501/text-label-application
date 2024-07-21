"""
view_contributer.py

Module for managing workflow contributors..

This module provides ViewSets for adding, removing, filtering, and retrieving
contributors for a workflow.

Classes:
    - ContributerModifyView: A ViewSet for adding, removing and filtering contributors in a workflow.
    - ContributerView: A ViewSet for retrieving contributors in a workflow.
"""

from rest_framework import authentication, viewsets
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from workflow_settings.permissions import (
    IsWorkflowCreatorPermission,
    WorkflowAccessPermission,
)
from workflow_settings.services.workflow_setting_service.contributer_service import (
    ContributerServiceClass,
)


class ContributerModifyView(viewsets.ViewSet):
    """
    ViewSet for adding, removing and filtering contributors in a workflow.

    Authentication Classes:
    - TokenAuthentication

    Permission Classes:
    - IsAuthenticated
    - IsWorkflowCreatorPermission

    Parser Classes:
    - JSONParser
    """

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated, IsWorkflowCreatorPermission]
    parser_class = [JSONParser]

    def remove_contributer_by_id(self, request, *args, **kwargs):
        """
        Remove a contributor from a workflow by their username.

        Path Parameters:
            - workflow_id (int): The ID of the workflow.

        Request Data:
            - username (string): Username of the contributer which should be removed.

        Returns:
            - Response: The HTTP response containing the status and a success message.

        Errors:
            - Response: A response containing the status and a error message.
        """
        workflow_id = kwargs["workflow_id"]
        contributer_username = request.data["username"]

        contributer_service = ContributerServiceClass()
        status, data = contributer_service.remove_contributer_by_id(
            workflow_id, contributer_username
        )

        return Response(status=status, data=data)

    def add_contributer_by_id(self, request, *args, **kwargs):
        """
        Add a contributor to a workflow by their username.

        Path Parameters:
            - workflow_id (int): The ID of the workflow.

        Request Data:
            - username (string): Username of the contributer which should be added.

        Returns:
            - Response: The HTTP response containing the status and a success message.

        Errors:
            - Response: A response containing the status and a error message.
        """
        workflow_id = kwargs["workflow_id"]
        contributer_username = request.data["username"]

        contributer_service = ContributerServiceClass()
        status, data = contributer_service.add_contributer_by_id(
            workflow_id, contributer_username
        )

        return Response(status=status, data=data)

    def filter_contributers(self, request, *args, **kwargs):
        """
        Filter contributors by their username by matching a string.

        Path Parameters::
            workflow_id (int): The ID of the workflow.

        Query Parameter:
            - username_start (string): Start of username of the contributer
                                       which is eeing searched for.

        Returns:
            - Response: The HTTP response containing the status and a list of
                        possible users by their unique usernames.

        Errors:
            - Response: A response containing the status and a error message.
        """
        workflow_id = kwargs["workflow_id"]
        request_user = request.user
        username_start = request.GET["username_start"]
        contributer_service = ContributerServiceClass()
        status, data = contributer_service.filter_contributer(
            workflow_id=workflow_id,
            request_user=request_user,
            username_start=username_start,
        )

        return Response(status=status, data=data)


class ContributerView(viewsets.ViewSet):
    """
    ViewSet for retrieving contributors in a workflow.

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

    def get_contributers(self, request, *args, **kwargs):
        """
        Retrieve all contributors of a workflow.

        Path Parameters:
            - workflow_id (int): The ID of the workflow.

        Returns:
            - Response: The HTTP response containing the status and a list of contributers.

        Errors:
            - Response: A response containing the status and a error message.
        """
        workflow_id = kwargs["workflow_id"]

        contributer_service = ContributerServiceClass()
        status, data = contributer_service.get_contributers(workflow_id=workflow_id)

        return Response(status=status, data=data)
