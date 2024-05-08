
from django.http import QueryDict
from rest_framework import status, authentication, viewsets
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from snorkel_flow_backend.settings import MEDIA_ROOT
from workflow_settings.permissions import WorkflowAccessPermission, IsWorkflowCreatorPermission
from workflow_settings.serializers.serializers_labelfunction import LabelfunctionCreateSerializer
from workflow_settings.serializers.serializers_workflow import WorkflowCreateSerializer, UserAddRelSerializers
from workflow_settings.services.labelfunktion_service.labelfunction_service import LabelfunctionService
from workflow_settings.services.workflow_setting_service.workflow_service import WorkflowServiceClass

class WorkflowAuthenticatetOnlyView(viewsets.ViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated]
    parser_class = [JSONParser]

    def get_access(self, request, *args, **kwargs):
        workflow_id = kwargs['workflow_id']
        workflowservice = WorkflowServiceClass()
        status, data = workflowservice.get_access(workflow_id, request.user)

        return Response(data=data, status=status)


    def create(self, request, *args, **kwargs):
        workflow = request.data['workflow']
        workflow['creator'] = UserAddRelSerializers(request.user).data['id']
        code_label = request.data['code_label']

        workflow_serializer = WorkflowCreateSerializer(data=workflow)

        workflowservice = WorkflowServiceClass()
        status_s, data = workflowservice.create(workflow_serializer)
        if status_s == status.HTTP_201_CREATED:
            labelfunction_import_standard = {'name': 'imports', 'type': 'import', 'code': 'from snorkel.labeling import labeling_function', 'workflow': data['workflow_id']}
            serialziers_import = LabelfunctionCreateSerializer(data=labelfunction_import_standard)
            labelfunction = LabelfunctionService()
            labelfunction.add_labelfunction(request.user, serialziers_import)

            labelfunction_labels = {'name': 'labels', 'type': 'labels',
                                             'code': code_label,
                                             'workflow': data['workflow_id']}
            serialziers_label = LabelfunctionCreateSerializer(data=labelfunction_labels)
            labelfunction = LabelfunctionService()
            labelfunction.add_labelfunction(request.user, serialziers_label)



        return Response(data=data, status=status_s)

    def list_all_by_user(self, request, *args, **kwargs):
        request_user = request.user
        workflowservice = WorkflowServiceClass()
        status, data = workflowservice.list_all_by_user(request_user)
        return Response(data=data, status=status)

# todo service hilfsfunktion später ausloagern aus workflow raus
    def get_installed_packages(self, request, *args, **kwargs):
        packages = []
        filepath = "{root}/../{name}".format(root=MEDIA_ROOT, name='requirements.txt')
        with open(filepath, 'r') as file:
            packages = file.readlines()
        return Response(packages, status=status.HTTP_200_OK)

class WorkflowView(viewsets.ViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated, WorkflowAccessPermission]
    parser_class = [JSONParser]

    def user_is_workflow_creator(self, request, *args, **kwargs):
        workflow_id = kwargs['workflow_id']
        request_user = request.user

        workflowservice = WorkflowServiceClass()
        status, data = workflowservice.user_is_workflow_creator(workflow_id, request_user)

        return Response(status=status, data=data)

    def get_by_id(self, request, *args, **kwargs):
        workflow_id = kwargs['workflow_id']

        workflowservice = WorkflowServiceClass()
        status, data = workflowservice.get_by_id(workflow_id)

        return Response(status=status, data=data)

    def delete_by_id(self, request, *args, **kwargs):
        self.permission_classes = [IsAuthenticated, IsWorkflowCreatorPermission]

        workflow_id = kwargs['workflow_id']

        workflowservice = WorkflowServiceClass()
        status, data = workflowservice.delete_by_id(workflow_id)

        return Response(status=status, data=data)

class WorkflowModifyView(viewsets.ViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated, IsWorkflowCreatorPermission]
    parser_class = [JSONParser]

    def update_by_id(self, request, *args, **kwargs):
        self.permission_classes = [IsAuthenticated, IsWorkflowCreatorPermission]

        workflow_id = kwargs['workflow_id']

        workflowservice = WorkflowServiceClass()
        status, data = workflowservice.update_by_id(workflow_id, request.data)

        return Response(status=status, data=data)






