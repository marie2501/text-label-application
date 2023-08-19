import json
import yaml

from django.contrib.auth.models import User
from django.http import QueryDict
from rest_framework import status, authentication, viewsets
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q, Count, QuerySet
from django.http import HttpResponseForbidden, HttpResponseNotFound, HttpResponseBadRequest

from workflow_settings.models import Workflow, Labelfunction, Labelfunction_Run
from workflow_settings.serializers.serializers_file import FileUploadLabelfunctionSerializer
from workflow_settings.serializers.serializers_labelfunction import LabelfunctionSerializer, LabelfunctionCreateSerializer
from workflow_settings.serializers.serializers_workflow import WorkflowSerializer, WorkflowCreateSerializer, UserAddRelSerializers


class LabelfunctionView(viewsets.ViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated]
    parser_class = [JSONParser]


    # File
    # Store the functions which are to be used in a run as a yml file
    # todo funktion noch nicht getestet
    def create_labelfunction_run(self, request, *args, **kwargs):
        workflow_id = kwargs['pk']
        file_serializer = FileUploadLabelfunctionSerializer(data=request.data)
        if file_serializer.is_valid():
            file = file_serializer.save(creator=request.user, workflow_id=workflow_id)
            return Response(status=status.HTTP_201_CREATED)
        return HttpResponseBadRequest()

    # todo funktion noch nicht getestet
    def get_labelfunction_run(self, request, *args, **kwargs):
        labelfunction_run_id = kwargs['pk']
        labelfunction_run = Labelfunction_Run.objects.filter(pk=labelfunction_run_id)
        if labelfunction_run.exists():
            l = labelfunction_run[0]
            with open(l.file.path, 'r') as file:
                yaml_content = yaml.safe_load(file)
            return Response(yaml_content, status=status.HTTP_200_OK)
        return HttpResponseNotFound()

    # todo execude function

    # Datenbank
    def get_all_labelfunction_by_workflow_id(self, request, *args, **kwargs):
        workflow_id = kwargs['pk']
        labelfunction = Labelfunction.objects.filter(workflow_id=workflow_id).order_by('creator')
        serialziers_label = LabelfunctionSerializer(labelfunction, many=True)
        return Response(serialziers_label.data, status=status.HTTP_200_OK)


    def add_labelfunction(self, request, *args, **kwargs):
        workflow_id = kwargs['pk']
        serialziers_label = LabelfunctionCreateSerializer(data=request.data)
        if serialziers_label.is_valid():
            serialziers_label.save(workflow_id=workflow_id, creator=request.user)
            return Response(status=status.HTTP_201_CREATED)
        return HttpResponseBadRequest()

    def delete_labelfunction(self, request, *args, **kwargs):
        labelfunction_id = kwargs['pk']
        labelfunction = Labelfunction.objects.filter(pk=labelfunction_id)
        if labelfunction.exists():
            l = labelfunction[0]
            if l.creator == request.user:
                l.delete()
                return Response(status=status.HTTP_200_OK)
            return HttpResponseForbidden()
        return HttpResponseNotFound()

    def update_labelfunction(self, request, *args, **kwargs):
        labelfunction_id = kwargs['pk']
        labelfunction = Labelfunction.objects.filter(pk=labelfunction_id)
        if labelfunction.exists():
            l = labelfunction[0]
            if l.creator == request.user:
                serialziers_label = LabelfunctionSerializer(l, data=request.data, partial=True)
                print(serialziers_label)
                if serialziers_label.is_valid():
                    serialziers_label.save()
                    return Response(status=status.HTTP_200_OK)
                return HttpResponseBadRequest()
            return HttpResponseForbidden()
        return HttpResponseNotFound()



