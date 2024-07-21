"""
file_upload_views.py

This module defines the API views for uploading and managing a dataset in a workflow.

Classes:
- FileUploadView: An API view for uploading, updating and checking
                  the status of a dataset in a workflow.

Methods:
- post(self, request, *args, **kwargs): Upload a new dataset to a workflow.
- put(self, request, *args, **kwargs): Replacing an existing dataset in a workflow.
- get(self, request, *args, **kwargs): Check whether a dataset has been uploaded to a workflow.
"""

from rest_framework import status, authentication
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from workflow_settings.permissions import IsWorkflowCreatorPermission
from workflow_settings.serializers.serializers_file import FileUploadSerializer
from workflow_settings.services.file_service.FileUploadService import FileUploadService


class FileUploadView(APIView):
    """
    API view for uploading, updating and checking a dataset in a workflow.

    This view uses token authentication and verifies that the user is authenticated
    and that the user is the creator of the workflow.

    Authentication classes:
    - TokenAuthentication

    Parser classes:
    - FileUploadParser

    Authorisation classes:
    - IsAuthenticated
    - IsWorkflowCreatorPermission
    """
    authentication_classes = [authentication.TokenAuthentication]
    parser_class = [FileUploadParser]
    permission_classes = [IsAuthenticated, IsWorkflowCreatorPermission]

    def post(self, request, *args, **kwargs):
        """
        Upload a new file (dataset) to a workflow.

        Path parameter:
        - workflow_id (int): The ID of the workflow to which the file is to be uploaded.

        Request data:
        - Form Data (file): dataset that fulfils a specified format.
        - user: user who made the request

        Return:
        - HTTP-Response: status code and {message: string}

        Error:
        - HTTP-Response: status code and {message: string} or serializer errors
        """
        workflow_id = kwargs["workflow_id"]
        file_serializer = FileUploadSerializer(data=request.data)
        request_user = request.user

        file_upload_service = FileUploadService()
        status_code, data = file_upload_service.upload_file(
            workflow_id=workflow_id,
            creator=request_user,
            file_serializer=file_serializer,
        )

        return Response(status=status_code, data=data)

    def put(self, request, *args, **kwargs):
        """
        Update an existing dataset in a workflow.

        Path parameter:
        - workflow_id (int): The ID of the workflow to which the file belongs.

        Request data:
        - Form Data (file): dataset that fulfils a specified format.
        - user: user who made the request

        Return:
        - HTTP-Response: status code and {message: string}

        Error:
        - HTTP-Response: status code and {message: string} or serializer errors
        """
        workflow_id = kwargs["workflow_id"]

        file_serializer = FileUploadSerializer(data=request.data)

        file_upload_service = FileUploadService()
        status_code, data = file_upload_service.update_file(
            workflow_id=workflow_id,
            file_serializer=file_serializer,
        )

        return Response(status=status_code, data=data)

    def get(self, request, *args, **kwargs):
        """
        Checks whether a data record has been uploaded in a workflow.

        Path parameter:
        - workflow_id (int): The ID of the workflow whose file upload status is to be checked.

        Return:
        - HTTP response: Contains the status of the file upload check as a boolean
        """
        workflow_id = kwargs["workflow_id"]

        file_upload_service = FileUploadService()
        data = file_upload_service.is_file_uploaded(workflow_id=workflow_id)

        return Response(data=data, status=status.HTTP_200_OK)
