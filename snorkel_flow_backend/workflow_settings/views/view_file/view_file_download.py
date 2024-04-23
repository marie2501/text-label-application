
from rest_framework import authentication
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from workflow_settings.permissions import RunAccessPermission
from workflow_settings.services.file_service.FileDownloadService import FileDownloadService


class FileDownloadView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    parser_class = [FileUploadParser]
    permission_classes = [IsAuthenticated, RunAccessPermission]

    def get(self, request, *args, **kwargs):
        run_id = kwargs['run_id']

        fileDownloadService = FileDownloadService()
        response, status, data = fileDownloadService.download_annotated_dataset(run_id)

        if response != None:
            return response
        return Response(status=status, data=data)

