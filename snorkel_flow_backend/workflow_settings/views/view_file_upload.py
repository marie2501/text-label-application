from rest_framework import status, authentication
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from workflow_settings.serializers.serializers_file import FileUploadSerializer
from workflow_settings.models import File, Workflow
from workflow_settings.services.FileUploadService import FileUploadService


# Dataset: corpus_id, entity_id, text, splitting_id

# todo sehr wichtig schreibe eigene permission klasse, sodas nur die läute in derm worklfow zugriff haben

class FileView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    parser_class = [FileUploadParser]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        workflow_id = kwargs['pk']
        file_serializer = FileUploadSerializer(data=request.data)
        request_user = request.user

        fileuploadService = FileUploadService()
        status_code, data = fileuploadService.upload_file(workflow_id=workflow_id, creator=request_user, file_serializer=file_serializer)

        return Response(status=status_code, data=data)


    def put(self, request, *args, **kwargs):
        workflow_id = kwargs['pk']
        file_serializer = FileUploadSerializer(data=request.data)
        request_user = request.user

        fileuploadService = FileUploadService()
        status_code, data = fileuploadService.update_file(workflow_id=workflow_id, creator=request_user, file_serializer=file_serializer)

        return Response(status=status_code, data=data)

    #todo auslagern und download machen keine filenamen get machen
    def get(self, request, *args, **kwargs):
        workflow_id = kwargs['pk']

        FileDownloadService
        return Response(status=status.HTTP_404_NOT_FOUND)

