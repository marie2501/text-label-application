"""
Module for managing workflows and labelfunctions through Django REST framework ViewSets.

This module provides ViewSets for authenticating access, creating workflows, listing workflows,
retrieving workflow details, updating workflows, deleting workflows, and managing labelfunctions.
It includes functionalities to manage workflows based on user permissions and access levels.

Classes:
    WorkflowAuthenticatetOnlyView: A ViewSet for handling workflow access and
                                   creation.
    WorkflowView: A ViewSet for retrieving, updating, and deleting workflows.
    WorkflowModifyView: A ViewSet for updating workflows by ID.
"""
import sys

from rest_framework import status, authentication, viewsets
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from snorkel_flow_backend.settings import MEDIA_ROOT
from workflow_settings.permissions import (
    WorkflowAccessPermission,
    IsWorkflowCreatorPermission,
)
from workflow_settings.serializers.serializers_labelfunction import (
    LabelfunctionCreateSerializer,
)
from workflow_settings.serializers.serializers_workflow import (
    WorkflowCreateSerializer,
    UserAddRelSerializers,
)
from workflow_settings.services.labelfunktion_service.labelfunction_service import (
    LabelfunctionService,
)
from workflow_settings.services.workflow_setting_service.workflow_service import (
    WorkflowServiceClass,
)


class WorkflowAuthenticatetOnlyView(viewsets.ViewSet):
    """
    ViewSet for handling workflow access and creation

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
        Authenticate access to a workflow.

        Path Parameters:
            - workflow_id (int): The ID of the workflow.

        Returns:
            - Response: A HTTP response containing the status and a boolean.
        """
        workflow_id = kwargs["workflow_id"]
        workflowservice = WorkflowServiceClass()
        status_code, data = workflowservice.get_access(workflow_id, request.user)

        return Response(data=data, status=status_code)

    def create(self, request, *args, **kwargs):
        """
        Create a new workflow and associated labelfunctions.

        Path Parameters:
            - workflow_id (int): The ID of the workflow.

        Returns:
            - Response: A HTTP response containing the status and the id of the created workflow.

        Errors:
            - Response: A HTTP response containing the status and a error message.
        """
        workflow = request.data["workflow"]
        workflow["creator"] = UserAddRelSerializers(request.user).data["id"]
        code_label = request.data["code_label"]

        workflow_serializer = WorkflowCreateSerializer(data=workflow)
        try:
            exec(code_label, locals())
        except:
            data = str(sys.exc_info())
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        workflowservice = WorkflowServiceClass()
        status_save, data = workflowservice.create(workflow_serializer)
        if status_save == status.HTTP_201_CREATED:
            labelfunction_import_standard = {
                "name": "imports",
                "type": "import",
                "code": "from snorkel.labeling import labeling_function",
                "workflow": data["workflow_id"],
            }
            serialziers_import = LabelfunctionCreateSerializer(
                data=labelfunction_import_standard
            )
            labelfunction = LabelfunctionService()
            labelfunction.add_labelfunction(request.user, serialziers_import)

            labelfunction_labels = {
                "name": "labels",
                "type": "labels",
                "code": code_label,
                "workflow": data["workflow_id"],
            }
            serialziers_label = LabelfunctionCreateSerializer(data=labelfunction_labels)
            labelfunction = LabelfunctionService()
            labelfunction.add_labelfunction(request.user, serialziers_label)

        return Response(data=data, status=status_save)

    def list_all_by_user(self, request, *args, **kwargs):
        """
        List all workflows of the authenticated user.

        Returns:
            - Response: A HTTP response containing the status and a list of workflow objects..
        """
        request_user = request.user
        workflowservice = WorkflowServiceClass()
        status_code, data = workflowservice.list_all_by_user(request_user)
        return Response(data=data, status=status_code)

    def get_installed_packages(self, request, *args, **kwargs):
        """
        Get the list of installed packages from the requirements file.

        Returns:
            - Response: A HTTP response containing the status and a list
                        of packages ans their version as string.
        """
        packages = []
        filepath = "{root}/../{name}".format(root=MEDIA_ROOT, name="requirements.txt")
        with open(filepath, "r") as file:
            packages = file.readlines()
        return Response(packages, status=status.HTTP_200_OK)


class WorkflowView(viewsets.ViewSet):
    """
    ViewSet for retrieving, updating, and deleting workflows.

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

    def user_is_workflow_creator(self, request, *args, **kwargs):
        """
        Check if the authenticated user is the creator of the workflow.

        Path Parameters:
            - workflow_id (int): The ID of the workflow.

        Returns:
            - Response: A HTTP response containing the status and a boolean.

        Errors:
            - Response: A HTTP response containing the status and a error message.
        """
        workflow_id = kwargs["workflow_id"]
        request_user = request.user

        workflowservice = WorkflowServiceClass()
        status_code, data = workflowservice.user_is_workflow_creator(
            workflow_id, request_user
        )

        return Response(status=status_code, data=data)

    def get_by_id(self, request, *args, **kwargs):
        """
        Retrieve a workflow by its ID.

        Path Parameters:
            - workflow_id (int): The ID of the workflow.

        Returns:
            - Response: A HTTP response containing the status and the workflow object.

        Errors:
            - Response: A HTTP response containing the status and a error message.
        """
        workflow_id = kwargs["workflow_id"]

        workflowservice = WorkflowServiceClass()
        status_code, data = workflowservice.get_by_id(workflow_id)

        return Response(status=status_code, data=data)

    def delete_by_id(self, request, *args, **kwargs):
        """
        Delete a workflow by its ID.

        Path Parameters:
            - workflow_id (int): The ID of the workflow.

        Returns:
            - Response: A HTTP response containing the status and a success message.

        Errors:
            - Response: A HTTP response containing the status and a error message.
        """
        self.permission_classes = [IsAuthenticated, IsWorkflowCreatorPermission]

        workflow_id = kwargs["workflow_id"]

        workflowservice = WorkflowServiceClass()
        status_code, data = workflowservice.delete_by_id(workflow_id)

        return Response(status=status_code, data=data)


class WorkflowModifyView(viewsets.ViewSet):
    """
    ViewSet for changing a workflow.

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

    def update_by_id(self, request, *args, **kwargs):
        """
        Update a workflow by its ID.

        Path Parameters:
            - workflow_id (int): The ID of the workflow.

        Returns:
            - Response: A HTTP response containing the status and the updated workflow object.

        Errors:
            - Response: A HTTP response containing the status and a error message.
        """
        self.permission_classes = [IsAuthenticated, IsWorkflowCreatorPermission]

        workflow_id = kwargs["workflow_id"]

        workflowservice = WorkflowServiceClass()
        status_code, data = workflowservice.update_by_id(workflow_id, request.data)

        return Response(status=status_code, data=data)
