"""
FileUploadService.py

The module provides a service that enables the upload of a file (dataset).

Classes:
- FileUploadService
"""
from rest_framework import status

from workflow_settings.models import File, Workflow


class FileUploadService:
    """
     Service provides functions for uploading and modifying files.
     It is also possible to check whether a file has been uploaded in a workflow.

    Methods:
        - upload_file(workflow_id, creator, file_serializer):
            Uploads a file to a specified workflow.

        - update_file(workflow_id, file_serializer):
            Updates an existing file in a specified workflow.

        - is_file_uploaded(workflow_id):
            Checks if a file is already uploaded for a specified workflow.
    """

    def upload_file(self, workflow_id, creator, file_serializer):
        """
        Uploads a file (dataset) to the specified workflow. File needs to have the
        colums ['corpus_id', 'entity_id', 'text', 'splitting_id', 'CLASS']

        Args:
            workflow_id (int): The ID of the workflow to which the file is to be uploaded.
            creator (User): The user who is uploading the file.
            file_serializer (FileSerializer): The serializer for the file being uploaded.

        Returns:
            - int: A HTTP status code.
            - dict: A dictionary containing a success message or error details.
        """
        workflow_filter = Workflow.objects.filter(pk=workflow_id)
        if workflow_filter.exists():
            if file_serializer.is_valid():
                file_serializer.save(creator=creator, workflow_id=workflow_id)
                return status.HTTP_201_CREATED, {
                    "message": "File was successfully created"
                }
            return status.HTTP_400_BAD_REQUEST, file_serializer.errors
        return status.HTTP_404_NOT_FOUND, {
            "message": "The workflow you want to access does not exist"
        }

    def update_file(self, workflow_id, file_serializer):
        """
        Updates a file (dataset) to the specified workflow. File needs to have the
        colums ['corpus_id', 'entity_id', 'text', 'splitting_id', 'CLASS']

        Args:
            workflow_id (int): The ID of the workflow to which the file is to be uploaded.
            file_serializer (FileSerializer): The serializer for the file being uploaded.

        Returns:
            - int: A HTTP status code.
            - dict: A dictionary containing a success message or error details.
        """
        file_filter = File.objects.filter(workflow_id=workflow_id)
        if file_filter.exists():
            file_object = file_filter[0]
            if file_serializer.is_valid():
                file_serializer.update(
                    instance=file_object, validated_data=file_serializer.validated_data
                )
                return status.HTTP_201_CREATED, {
                    "message": "File was successfully updated"
                }
            return status.HTTP_403_FORBIDDEN, file_serializer.errors
        return status.HTTP_404_NOT_FOUND, {
            "message": "The file you want to update does not exist"
        }

    def is_file_uploaded(self, workflow_id):
        """
        Checks if a file is already uploaded for a specified workflow.

        Args:
            workflow_id (int): The ID of the workflow to be checked

        Returns:
            - bool: True if a file has already been uploaded, otherwise False
        """
        file_filter = File.objects.filter(workflow_id=workflow_id)
        if file_filter.exists():
            return True
        return False
