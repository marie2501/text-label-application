import json

from django.http import QueryDict
from rest_framework import status, authentication, viewsets
from rest_framework.parsers import FileUploadParser, JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from workflow_settings.models import Workflow
from workflow_settings.serializers.serializers_workflow import WorkflowSerializer, WorkflowCreateSerializer, UserSerializers




class WorkflowView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated]
    parser_class = [JSONParser]


# todo testen, und dafür sorgen das Datenpunkte in Datenbanken eingelesen werden
    def post(self, request, *args, **kwargs):
        if isinstance(request.data, QueryDict):
            request.data._mutable = True
        request.data['creator'] = UserSerializers(request.user).data['id']
        workflow_serializer = WorkflowCreateSerializer(data=request.data)
        if workflow_serializer.is_valid():
            workflow = workflow_serializer.save()
            return Response({'workflow_id': workflow.id},status=status.HTTP_201_CREATED)
        else:
            return Response(workflow_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def get(self, request, *args, **kwargs):
        workflows = Workflow.objects.filter(creator=request.user)
        serialziers_workflow = WorkflowSerializer(workflows, many=True)
        return Response(serialziers_workflow.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        workflow_id = request.data['workflow_id']
        Workflow.objects.get(pk=workflow_id).delete()
        return Response(status=status.HTTP_200_OK)


