from rest_framework.permissions import BasePermission

from workflow_settings.models import Workflow, Run, Labelfunction


# View authorization: Only for workflow creators and workflow contributors
class WorkflowAccessPermission(BasePermission):

    def has_permission(self, request, view):
        workflow_id = view.kwargs.get('workflow_id')
        request_user = request.user

        workflow_filter = Workflow.objects.filter(pk=workflow_id)
        if workflow_filter.exists():
            workflow_object = workflow_filter[0]
            if (request_user == workflow_object.creator) or (request_user.username in workflow_object.contributors.values_list('username', flat=True)):
                return True
        return False

# View authorization: Only for workflow creators and workflow contributors
class IsWorkflowCreatorPermission(BasePermission):

    def has_permission(self, request, view):
        workflow_id = view.kwargs.get('workflow_id')
        request_user = request.user

        workflow_filter = Workflow.objects.filter(pk=workflow_id)
        if workflow_filter.exists():
            workflow_object = workflow_filter[0]
            if request_user == workflow_object.creator:
                return True
        return False
class IsLabelfuntionCreatorPermission(BasePermission):

    def has_permission(self, request, view):
        labelfunction_id = view.kwargs.get('labelfunction_id')
        request_user = request.user

        labelfunction_filter = Labelfunction.objects.filter(pk=labelfunction_id)
        if labelfunction_filter.exists():
            labelfunction_object = labelfunction_filter[0]
            if request_user == labelfunction_object.creator:
                return True
        return False

# View authorization: Only for run creators
class IsRunCreatorPermission(BasePermission):

    def has_permission(self, request, view):
        run_id = view.kwargs.get('run_id')
        request_user = request.user

        run_filter = Run.objects.filter(pk=run_id)
        if run_filter.exists():
            run_object = run_filter[0]
            if request_user == run_object.creator:
                return True
        return False



