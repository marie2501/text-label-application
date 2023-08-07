from rest_framework import status, authentication
from rest_framework.parsers import FileUploadParser, JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from workflow_settings.serializers.serializers_file import FileUploadSerializer
from workflow_settings.models import Workflow


class FileUploadView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    parser_class = [FileUploadParser]
    permission_classes = [IsAuthenticated]


# todo testen, und dafür sorgen das Datenpunkte in Datenbanken eingelesen werden
    def post(self, request, *args, **kwargs):
        workflow_id = request.data['workflow_id']
        file_serializer = FileUploadSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save(creator=request.user, workflow_id=workflow_id)
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


