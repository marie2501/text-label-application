import sys

from snorkel.labeling import PandasLFApplier, LFAnalysis
import pandas as pd

from zen_queries import fetch, queries_disabled

from rest_framework import status, authentication, viewsets
from rest_framework.parsers import JSONParser, FileUploadParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from snorkel_flow_backend.settings import MEDIA_ROOT
from workflow_settings.models import Labelfunction, File, Run
from workflow_settings.permissions import IsLabelfuntionCreatorPermission, WorkflowAccessPermission
from workflow_settings.serializers.serializers_labelfunction import LabelfunctionSerializer, LabelfunctionCreateSerializer
from workflow_settings.services.labelfunktion_service.labelfunction_service import LabelfunctionService


class LabelfunctionView(viewsets.ViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated, WorkflowAccessPermission]
    parser_class = [JSONParser]

    def get_imports(self, request, *args, **kwargs):
        workflow_id = kwargs['workflow_id']

        labelfunction = LabelfunctionService()
        status, data = labelfunction.get_imports(workflow_id)

        return Response(status=status, data=data)

    def compile_labelfunction(self, request, *args, **kwargs):
        code = request.data['pythoncode']
        workflow_id = kwargs['workflow_id']

        labelfunction = LabelfunctionService()
        status, data = labelfunction.compile_labelfunction(workflow_id, code)

        return Response(status=status, data=data)


    # Imports und Code werden unter locals ausgeführt
    def test_labelfunction(self, request, *args, **kwargs):
        workflow_id = kwargs['workflow_id']
        code = request.data['pythoncode']
        name = request.data['name']

        labelfunction = LabelfunctionService()
        status, data = labelfunction.test_labelfunction(workflow_id, code, name)

        return Response(status=status, data=data)

    def get_all_labelfunction_by_workflow_id(self, request, *args, **kwargs):
        workflow_id = kwargs['workflow_id']

        labelfunction = LabelfunctionService()
        status, data = labelfunction.get_all_labelfunction_by_workflow_id(workflow_id)
        return Response(status=status, data=data)


    def add_labelfunction(self, request, *args, **kwargs):
        workflow_id = kwargs['workflow_id']
        request_data = request.data
        request_data['workflow'] = workflow_id
        serialziers_label = LabelfunctionCreateSerializer(data=request_data)

        labelfunction = LabelfunctionService()
        status, data = labelfunction.add_labelfunction(request.user, serialziers_label)
        return Response(status=status, data=data)

class LabelfunctionModifyView(viewsets.ViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated, IsLabelfuntionCreatorPermission]
    parser_class = [JSONParser]

    def get_labelfunction_by_id(self, request, *args, **kwargs):
        labelfunction_id = kwargs['labelfunction_id']

        labelfunction = LabelfunctionService()
        status, data = labelfunction.get_labelfunction_by_id(labelfunction_id)

        return Response(status=status, data=data)

    def delete_labelfunction(self, request, *args, **kwargs):
        labelfunction_id = kwargs['labelfunction_id']

        labelfunction = LabelfunctionService()
        status, data = labelfunction.delete_labelfunction(labelfunction_id)
        return Response(status=status, data=data)

    def update_labelfunction(self, request, *args, **kwargs):
        labelfunction_id = kwargs['labelfunction_id']
        request_data = request.data

        labelfunction = LabelfunctionService()
        status, data = labelfunction.update_labelfunction(labelfunction_id, request_data)
        return Response(status=status, data=data)
