"""
file_download_views.py

This module defines the API views for downloading annotated data records.

Classes:
- FileDownloadView: An API view for downloading an annotated
                    annotated dataset for a specific run.

Methods:
- get(self, request, *args, **kwargs): Returns the annotated data set of a run.
"""

from rest_framework import authentication
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from workflow_settings.permissions import IsRunCreatorPermission
from workflow_settings.services.file_service.FileDownloadService import (
    FileDownloadService,
)


class FileDownloadView(APIView):
    """
    API view for downloading an annotated data set for a specific run.

    This view uses token authentication and verifies that the user is authenticated
    and that the user is the creator of the run.

    Authentication classes:
    - TokenAuthentication

    Parser classes:
    - FileUploadParser

    Authorisation classes:
    - IsAuthenticated
    - IsRunCreatorPermission
    """

    authentication_classes = [authentication.TokenAuthentication]
    parser_class = [FileUploadParser]
    permission_classes = [IsAuthenticated, IsRunCreatorPermission]

    def get(self, request, *args, **kwargs):
        """
        Returns the annotated data set of a run.

        Prerequisite:
        A classifier must be trained beforehand.

        Path parameter:
        - run_id (int): The ID of the run that is to be considered.

        Return:
        - HTTP response: Contains the annotated file as a blob object.
        - HTTP status and data in the event of an error.
        """
        run_id = kwargs["run_id"]

        file_download_service = FileDownloadService()
        response, status, data = file_download_service.download_annotated_dataset(
            run_id
        )

        if response is not None:
            return response
        return Response(status=status, data=data)
