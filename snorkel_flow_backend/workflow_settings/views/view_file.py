from django.http import HttpResponseNotFound
from rest_framework import status, authentication
from rest_framework.parsers import FileUploadParser, JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
import pandas as pd

from snorkel_flow_backend.settings import MEDIA_ROOT
from workflow_settings.serializers.serializers_file import FileUploadSerializer, FileUpdateSerializer
from workflow_settings.models import File

# Dataset: corpus_id, entity_id, text, splitting_id

class FileView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    parser_class = [FileUploadParser]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        workflow_id = kwargs['pk']
        file_serializer = FileUploadSerializer(data=request.data)
        if file_serializer.is_valid():
            file = file_serializer.save(creator=request.user, workflow_id=workflow_id)
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        workflow_id = kwargs['pk']
        file = File.objects.get(workflow_id=workflow_id)
        file_serializer = FileUploadSerializer(data=request.data)
        if file.creator == request.user:
            if file_serializer.is_valid():
                file = file_serializer.update(instance=file, validated_data=file_serializer.validated_data)
                return Response(status=status.HTTP_201_CREATED)
            else:
                return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def get(self, request, *args, **kwargs):
        workflow_id = kwargs['pk']
        files = File.objects.filter(workflow_id=workflow_id)
        if files.exists():
            file_objects = []
            for f in files:
                file_dict = {}
                file_dict['name'] = f.__str__()
                file_dict['id'] = f.id
                file_objects.append(file_dict)
            return Response(file_objects[0], status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

