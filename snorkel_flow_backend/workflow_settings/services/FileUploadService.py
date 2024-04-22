from rest_framework import status

from workflow_settings.models import File, Workflow


class FileUploadService:

    def upload_file(self, workflow_id, creator, file_serializer):
        workflow_filter = Workflow.objects.filter(pk=workflow_id)
        if workflow_filter.exists():
            if file_serializer.is_valid():
                file_serializer.save(creator=creator, workflow_id=workflow_id)
                return status.HTTP_201_CREATED, {"message": "File was successfully created"}
            return status.HTTP_400_BAD_REQUEST, file_serializer.errors
        return status.HTTP_404_NOT_FOUND, {"message": "The workflow you want to access does not exist"}

    def update_file(self, workflow_id, creator, file_serializer):
        file_filter = File.objects.filter(workflow_id=workflow_id)
        if file_filter.exists():
            file_object = file_filter[0]
            if file_serializer.is_valid():
                file_serializer.update(instance=file_object, validated_data=file_serializer.validated_data)
                return status.HTTP_201_CREATED, {"message": "File was successfully updated"}
            return status.HTTP_403_FORBIDDEN, {"message": "You do not have the authorization to change the data set"}

    def is_file_uploaded(self, workflow_id):
        file_filter = File.objects.filter(workflow_id=workflow_id)
        if file_filter.exists():
            return True
        return False

