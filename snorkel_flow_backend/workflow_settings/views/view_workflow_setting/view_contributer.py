
from rest_framework import authentication, viewsets
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from workflow_settings.permissions import IsWorkflowCreatorPermission, WorkflowAccessPermission
from workflow_settings.services.workflow_setting_service.contributer_service import ContributerServiceClass


# todo passe das Frontend dazu an - contributer für alle sichtbar uaf dem dashboard, für ceator durch klicken wird löschen möglich + felg mit add user,
# todo das verweist auf ein bedingung feld dort wird username gefiltert.
class ContributerModifyView(viewsets.ViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated, IsWorkflowCreatorPermission]
    parser_class = [JSONParser]



    #todo view contributer change frontend anzeigen user wurde 2 methoden achte darauf das nur creatot user sieht
    def remove_contributer_by_id(self, request, *args, **kwargs):
        workflow_id = kwargs['workflow_id']
        contributer_username = request.data['username']

        contributerService = ContributerServiceClass()
        status, data = contributerService.remove_contributer_by_id(workflow_id,contributer_username)

        return Response(status=status, data=data)

    def add_contributer_by_id(self, request, *args, **kwargs):
        workflow_id = kwargs['workflow_id']
        contributer_username = request.data['username']

        contributerService = ContributerServiceClass()
        status, data = contributerService.add_contributer_by_id(workflow_id,contributer_username)

        return Response(status=status, data=data)

    def filter_contributers(self, request, *args, **kwargs):
        workflow_id = kwargs['workflow_id']
        request_user = request.user
        username_start = request.data['username_start']
        contributerService = ContributerServiceClass()
        status, data = contributerService.filter_contributer(workflow_id=workflow_id, request_user=request_user, username_start=username_start)

        return Response(status=status, data=data)

class ContributerView(viewsets.ViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated, WorkflowAccessPermission]
    parser_class = [JSONParser]

    def get_contributers(self, request, *args, **kwargs):
        workflow_id = kwargs['workflow_id']

        contributerService = ContributerServiceClass()
        status, data = contributerService.get_contributers(workflow_id=workflow_id)

        return Response(status=status, data=data)






