"""
workflow_service.py

The module provides a service that enables the management of Workflows.

Classes:
- WorkflowServiceClass
"""

from django.db.models import Q
from rest_framework import status

from workflow_settings.models import Workflow
from workflow_settings.serializers.serializers_workflow import WorkflowSerializer


class WorkflowServiceClass:
    """
    Service class for creating, managing and accessing workflows.

    Methods:
        - get_access(workflow_id, request_user):
            Checks if a user has access to a specified workflow.

        - create(workflow_serializer):
            Creates a new workflow.

        - list_all_by_user(request_user):
            Lists all workflows associated with a user.

        - user_is_workflow_creator(workflow_id, request_user):
            Checks if the user is the creator of the specified workflow.

        - get_by_id(workflow_id):
            Retrieves a workflow by its ID.

        - delete_by_id(workflow_id):
            Deletes a workflow by its ID.

        - update_by_id(workflow_id, request_data):
            Updates a workflow by its ID with the provided data.
    """

    def get_access(self, workflow_id, request_user):
        """
        Checks whether a user is authorised to access a workflow

        Args:
            workflow_id (int): The ID of the workflow.
            request_user (User): The user who wants to access the workflow.

        Returns:
            - int: A HTTP status code.
            - bool: True if the user gets access, otherwise False
        """
        workflow_filter = Workflow.objects.filter(pk=workflow_id)
        if workflow_filter.exists():
            workflow_object = workflow_filter[0]
            if (request_user == workflow_object.creator) or (
                request_user.username
                in workflow_object.contributors.values_list("username", flat=True)
            ):
                return status.HTTP_200_OK, True
        return status.HTTP_200_OK, False

    def create(self, workflow_serializer):
        """
        Creates a new workflow.

        Args:
            workflow_serializer (workflow_serializer): The serialized workflow
                                                       object which should be created.

        Returns:
            - int: A HTTP status code.
            - dict:
                success: The ID of the created workflow
                error: A error message.
        """
        if workflow_serializer.is_valid():
            workflow = workflow_serializer.save()
            return status.HTTP_201_CREATED, {"workflow_id": workflow.id}
        return status.HTTP_400_BAD_REQUEST, workflow_serializer.errors

    def list_all_by_user(self, request_user):
        """
        List all the workflows of a specific user.

        Args:
            request_user (User): The user who makes the request.

        Returns:
            - int: A HTTP status code.
            - list: List of workflow objects.
        """
        workflows = Workflow.objects.filter(
            Q(creator=request_user) | Q(contributors=request_user)
        ).distinct()
        serialziers_workflow = WorkflowSerializer(workflows, many=True)
        return status.HTTP_200_OK, serialziers_workflow.data

    def user_is_workflow_creator(self, workflow_id, request_user):
        """
        Checks whether a user is the workflow creator.

        Args:
            workflow_id (int): The ID of the workflow.
            request_user (User): The user who wants to access the workflow.

        Returns:
            - int: A HTTP status code.
            - dict: Returns dict with a bool. True if the user is the creator, otherwise False
            - dict: In the case of a error a error message will be returned
        """
        workflow = Workflow.objects.filter(pk=workflow_id)
        if workflow.exists():
            if workflow[0].creator == request_user:
                return status.HTTP_200_OK, {"isCreator": True}
            return status.HTTP_200_OK, {"isCreator": False}
        return status.HTTP_404_NOT_FOUND, {
            "message": "The workflow you want to access does not exist"
        }

    def get_by_id(self, workflow_id):
        """
        Retrieves a specific workflow.

        Args:
            workflow_id (int): The ID of the workflow.

        Returns:
            - int: A HTTP status code.
            - success: workflow object
            - error: dict with error message
        """
        workflow = Workflow.objects.filter(pk=workflow_id)
        if workflow.exists():
            serialziers_workflow = WorkflowSerializer(workflow[0])
            return status.HTTP_200_OK, serialziers_workflow.data
        return status.HTTP_404_NOT_FOUND, {
            "message": "The workflow you want to access does not exist"
        }

    def delete_by_id(self, workflow_id):
        """
        Deletes a specific workflow.

        Args:
            workflow_id (int): The ID of the workflow.

        Returns:
            - int: A HTTP status code.
            - dict: A dict with a success or error message.
        """
        workflow = Workflow.objects.filter(pk=workflow_id)
        if workflow.exists():
            workflow[0].delete()
            return status.HTTP_200_OK, {
                "message": "The workflow was successfuly deleted"
            }
        return status.HTTP_404_NOT_FOUND, {
            "message": "The workflow you want to access does not exist"
        }

    def update_by_id(self, workflow_id, request_data):
        """
        Updates a specific workflow using its ID

        Args:
            workflow_id (int): The ID of the workflow.
            request_data (Workflow): The workflow object to be updated.

        Returns:
            - int: A HTTP status code.
            - success: updated workflow object
            - error: dict with error message
        """
        workflow = Workflow.objects.filter(pk=workflow_id)
        if workflow.exists():
            w = workflow[0]
            workflow_serializer = WorkflowSerializer(w, data=request_data, partial=True)
            if workflow_serializer.is_valid():
                workflow_serializer.save()
                return status.HTTP_200_OK, workflow_serializer.data
            return status.HTTP_400_BAD_REQUEST, workflow_serializer.errors
        return status.HTTP_404_NOT_FOUND, {
            "message": "The workflow you want to access does not exist"
        }
