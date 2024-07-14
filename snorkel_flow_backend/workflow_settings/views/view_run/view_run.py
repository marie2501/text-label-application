
from rest_framework import authentication, viewsets, status
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from workflow_settings.permissions import WorkflowAccessPermission, IsRunCreatorPermission
from workflow_settings.serializers.serializers_run import RunCreateSerializer
from workflow_settings.services.run_service.run_service import RunService


class RunAuthenticateView(viewsets.ViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated]
    parser_class = [JSONParser]

    def get_access(self, request, *args, **kwargs):
        run_id = kwargs['run_id']

        runservice = RunService()
        status, data = runservice.get_access(run_id, request.user)

        return Response(data=data, status=status)

class RunView(viewsets.ViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated, IsRunCreatorPermission]
    parser_class = [JSONParser]

    def exec_run(self, request, *args, **kwargs):
        run_id = kwargs['run_id']

        runservice = RunService()
        status, data, L_train_train, dataframe_train, labelfunction_names = runservice.exec_run(run_id)

        return Response(status=status, data=data)

    def get_run_by_id(self, request, *args, **kwargs):
        run_id = kwargs['run_id']

        runservice = RunService()
        status, data = runservice.get_run(run_id)

        return Response(status=status, data=data)

    def update_run(self, request, *args, **kwargs):
        run_id = kwargs['run_id']

        runservice = RunService()
        status, data = runservice.update_run(run_id, request.data)

        return Response(status=status, data=data)



class RunCreateView(viewsets.ViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated, WorkflowAccessPermission]
    parser_class = [JSONParser]


    def create_run(self, request, *args, **kwargs):
        workflow_id = kwargs['workflow_id']
        print(request.data)

        run_serializer = RunCreateSerializer(data=request.data)

        runservice = RunService()
        status, data = runservice.create_run(workflow_id, run_serializer, request.user)

        print(status)
        print(data)

        return Response(status=status, data=data)

    def list_run(self, request, *args, **kwargs):
        workflow_id = kwargs['workflow_id']

        runservice = RunService()
        status, data = runservice.list_run(workflow_id, request.user)

        return Response(status=status, data=data)


