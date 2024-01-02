import json

from django.contrib.auth.models import User
from django.http import QueryDict
from rest_framework import status, authentication, viewsets
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q
from django.http import HttpResponseForbidden, HttpResponseNotFound

from workflow_settings.models import Workflow
from workflow_settings.serializers.serializers_labelfunction import LabelfunctionCreateSerializer
from workflow_settings.serializers.serializers_workflow import WorkflowSerializer, WorkflowCreateSerializer, UserAddRelSerializers


class WorkflowView(viewsets.ViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated]
    parser_class = [JSONParser]


# todo testen, und dafür sorgen das Datenpunkte in Datenbanken eingelesen werden
    def create(self, request, *args, **kwargs):
        if isinstance(request.data, QueryDict):
            request.data._mutable = True
        request.data['creator'] = UserAddRelSerializers(request.user).data['id']
        workflow_serializer = WorkflowCreateSerializer(data=request.data)
        if workflow_serializer.is_valid():
            workflow = workflow_serializer.save()
            labelfunction_import_standard = {'name' : 'imports', 'type': 'import', 'code': 'from snorkel.labeling import labeling_function', 'workflow': workflow.id}
            serialziers_label = LabelfunctionCreateSerializer(data=labelfunction_import_standard)
            if serialziers_label.is_valid():
                serialziers_label.save(creator=request.user)
            return Response({'workflow_id': workflow.id}, status=status.HTTP_201_CREATED)
        return Response(workflow_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list_all_by_user(self, request, *args, **kwargs):
        workflows = Workflow.objects.filter(Q(creator=request.user) | Q(contributors=request.user)).distinct()
        serialziers_workflow = WorkflowSerializer(workflows, many=True)
        return Response(serialziers_workflow.data, status=status.HTTP_200_OK)

    def user_is_workflow_creator(self, request, *args, **kwargs):
        workflow_id = kwargs['pk']
        workflow = Workflow.objects.filter(pk=workflow_id)
        if workflow.exists():
            if workflow[0].creator == request.user:
                return Response({'isCreator': True }, status=status.HTTP_200_OK)
            return Response({'isCreator': False}, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def get_by_id(self, request, *args, **kwargs):
        workflow_id = kwargs['pk']
        workflow = Workflow.objects.filter(pk=workflow_id)
        if workflow.exists():
            if (workflow[0].creator == request.user) or \
                    (str(request.user) in list(workflow[0].contributors.values_list('username', flat=True))) or \
                    (workflow[0].is_public == True):
                serialziers_workflow = WorkflowSerializer(workflow[0])
                return Response(serialziers_workflow.data, status=status.HTTP_200_OK)
            else:
                return HttpResponseForbidden()
        else:
            return HttpResponseNotFound()

    def delete_by_id(self, request, *args, **kwargs):
        workflow_id = kwargs['pk']
        workflow = Workflow.objects.filter(pk=workflow_id)
        if workflow.exists():
            if workflow[0].creator == request.user:
                workflow[0].delete()
                return Response(status=status.HTTP_200_OK)
            else:
                return HttpResponseForbidden()
        else:
            return HttpResponseNotFound()


    def update_by_id(self, request, *args, **kwargs):
        workflow_id = kwargs['pk']
        workflow = Workflow.objects.filter(pk=workflow_id)
        if workflow.exists():
            w = workflow[0]
            workflow_serializer = WorkflowSerializer(w, data=request.data, partial=True)
            if workflow_serializer.is_valid():
                workflow_serializer.save()
                return Response(workflow_serializer.data, status=status.HTTP_200_OK)
            return Response(workflow_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return HttpResponseNotFound()



    def remove_contributer_by_id(self, request, *args, **kwargs):
        workflow_id = kwargs['pk']
        contributer_username = request.data['username']
        print(request.data)
        workflow = Workflow.objects.filter(pk=workflow_id)
        if workflow.exists():
            if workflow[0].creator == request.user:
                user = workflow[0].contributors.filter(username=contributer_username)
                if user.exists():
                    workflow[0].contributors.remove(user[0])
                    return Response(status=status.HTTP_200_OK)
                else:
                    return HttpResponseNotFound()
            else:
                return HttpResponseForbidden()
        else:
            return HttpResponseNotFound()

    def add_contributer_by_id(self, request, *args, **kwargs):
        workflow_id = kwargs['pk']
        contributer_username = request.data['username']
        workflow = Workflow.objects.filter(pk=workflow_id)
        if workflow.exists():
            if workflow[0].creator == request.user:
                user = User.objects.filter(username=contributer_username)
                if user.exists():
                    if not workflow[0].contributors.filter(username=user[0].username).exists():
                        workflow[0].contributors.add(user[0])
                        return Response(status=status.HTTP_200_OK)
                    else:
                        return Response(status=status.HTTP_400_BAD_REQUEST)
                else:
                    return HttpResponseNotFound()
            else:
                return HttpResponseForbidden()
        else:
            return HttpResponseNotFound()

    def get_all_users(self, request, *args, **kwargs):
        workflow_id = kwargs['pk']
        workflow = Workflow.objects.filter(pk=workflow_id)
        if workflow.exists():
            workflow = workflow[0]
            workflow_contributer = workflow.contributors.order_by('username').values_list('username', flat=True)

            all_contributer = []
            for contributer in workflow_contributer:
                dic = {}
                dic['label'] = 'contributer'
                dic['value'] = contributer
                all_contributer.append(dic)
            all_contributer.append({'label': 'contributer', 'value': workflow.creator.username})

            all_users = []
            if workflow.creator == request.user:
                users_not_contributer = User.objects.filter(Q(is_staff=False), ~Q(username=request.user), ~Q(username__in=workflow_contributer)).order_by('username').values_list('username', flat=True)

                all_users = []
                for contributer in users_not_contributer:
                    dic = {}
                    dic['label'] = 'user'
                    dic['value'] = contributer
                    all_users.append(dic)
            return Response([{'label': 'contributer', 'items': all_contributer}, {'label': 'user', 'items': all_users}],status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)







