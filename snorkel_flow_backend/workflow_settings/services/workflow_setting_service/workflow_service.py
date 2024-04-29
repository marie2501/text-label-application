from django.db.models import Q
from rest_framework import status

from workflow_settings.models import Workflow
from workflow_settings.serializers.serializers_workflow import WorkflowSerializer


class WorkflowServiceClass:

    def get_access(self, workflow_id, request_user):
        workflow_filter = Workflow.objects.filter(pk=workflow_id)
        if workflow_filter.exists():
            workflow_object = workflow_filter[0]
            if (request_user == workflow_object.creator) or (request_user.username in workflow_object.contributors.values_list('username', flat=True)):
                return status.HTTP_200_OK, True
        return status.HTTP_200_OK, False

    def create(self, workflow_serializer):
        if workflow_serializer.is_valid():
            workflow = workflow_serializer.save()
            return status.HTTP_201_CREATED, {'workflow_id': workflow.id}
        return status.HTTP_400_BAD_REQUEST, workflow_serializer.errors

    def list_all_by_user(self, request_user):
        workflows = Workflow.objects.filter(Q(creator=request_user) | Q(contributors=request_user)).distinct()
        serialziers_workflow = WorkflowSerializer(workflows, many=True)
        return status.HTTP_200_OK, serialziers_workflow.data

    def user_is_workflow_creator(self, workflow_id, request_user):
        workflow = Workflow.objects.filter(pk=workflow_id)
        if workflow.exists():
            if workflow[0].creator == request_user:
                return status.HTTP_200_OK, {'isCreator': True}
            return status.HTTP_200_OK, {'isCreator': False}
        return status.HTTP_404_NOT_FOUND, {"message": "The workflow you want to access does not exist"}

    def get_by_id(self, workflow_id):
        workflow = Workflow.objects.filter(pk=workflow_id)
        if workflow.exists():
            serialziers_workflow = WorkflowSerializer(workflow[0])
            return status.HTTP_200_OK, serialziers_workflow.data
        return status.HTTP_404_NOT_FOUND, {"message": "The workflow you want to access does not exist"}

    def delete_by_id(self, workflow_id):
        workflow = Workflow.objects.filter(pk=workflow_id)
        if workflow.exists():
            workflow[0].delete()
            return status.HTTP_200_OK, {"message": "The workflow was successfuly deleted"}
        return status.HTTP_404_NOT_FOUND, {"message": "The workflow you want to access does not exist"}

    def update_by_id(self, workflow_id, request_data):
        workflow = Workflow.objects.filter(pk=workflow_id)
        if workflow.exists():
            w = workflow[0]
            workflow_serializer = WorkflowSerializer(w, data=request_data, partial=True)
            if workflow_serializer.is_valid():
                workflow_serializer.save()
                return status.HTTP_200_OK, workflow_serializer.data
            return status.HTTP_400_BAD_REQUEST, workflow_serializer.errors
        return status.HTTP_404_NOT_FOUND, {"message": "The workflow you want to access does not exist"}