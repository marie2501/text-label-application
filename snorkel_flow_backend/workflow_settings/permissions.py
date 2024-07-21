"""
Module for defining custom permissions for workflow, labelfunction, and run access control.

This module provides custom permissions to control access based on the user's relationship
to the workflow, labelfunction, or run. It includes permissions for workflow creators, workflow
contributors, labelfunction creators, and run creators.

Classes:
    - WorkflowAccessPermission: Permission class for workflow creators and contributors.
    - IsWorkflowCreatorPermission: Permission class for workflow creators only.
    - IsLabelfuntionCreatorPermission: Permission class for labelfunction creators.
    - IsRunCreatorPermission: Permission class for run creators.
"""

from rest_framework.permissions import BasePermission
from workflow_settings.models import Workflow, Run, Labelfunction


class WorkflowAccessPermission(BasePermission):
    """
    Permission class for workflow creators and contributors.

    This class grants access to the view if the user is either the creator of the workflow
    or a contributor to the workflow.

    Methods:
        has_permission(request, view): Checks if the user has access to the workflow.
    """

    def has_permission(self, request, view):
        """
        Check if the user has access to the workflow.

        Returns:
            bool: True if if the user is either the creator or a contributor
                  to the workflow, False otherwise.
        """
        workflow_id = view.kwargs.get("workflow_id")
        request_user = request.user

        workflow_filter = Workflow.objects.filter(pk=workflow_id)
        if workflow_filter.exists():
            workflow_object = workflow_filter[0]
            if (request_user == workflow_object.creator) or (
                request_user.username
                in workflow_object.contributors.values_list("username", flat=True)
            ):
                return True
        return False


class IsWorkflowCreatorPermission(BasePermission):
    """
    Permission class for workflow creators only.

    This class grants access to the view only if the user is the creator of the workflow.

    Methods:
        has_permission(request, view): Checks if the user is the creator of the workflow.
    """

    def has_permission(self, request, view):
        """
        Check if the user is the creator of the workflow.

        Returns:
            bool: True if the user is the creator, False otherwise.
        """
        workflow_id = view.kwargs.get("workflow_id")
        request_user = request.user

        workflow_filter = Workflow.objects.filter(pk=workflow_id)
        if workflow_filter.exists():
            workflow_object = workflow_filter[0]
            if request_user == workflow_object.creator:
                return True
        return False


class IsLabelfuntionCreatorPermission(BasePermission):
    """
    Permission class for labelfunction creators.

    This class grants access to the view only if the user is the creator of the labelfunction.

    Methods:
        has_permission(request, view): Checks if the user is the creator of the labelfunction.
    """

    def has_permission(self, request, view):
        """
        Check if the user is the creator of the labelfunction.

        Returns:
            bool: True if the user is the creator of the labelfunction, False otherwise.
        """
        labelfunction_id = view.kwargs.get("labelfunction_id")
        request_user = request.user

        labelfunction_filter = Labelfunction.objects.filter(pk=labelfunction_id)
        if labelfunction_filter.exists():
            labelfunction_object = labelfunction_filter[0]
            if request_user == labelfunction_object.creator:
                return True
        return False


class IsRunCreatorPermission(BasePermission):
    """
    Permission class for run creators.

    This class grants access to the view only if the user is the creator of the run.

    Methods:
        has_permission(request, view): Checks if the user is the creator of the run.
    """

    def has_permission(self, request, view):
        """
        Check if the user is the creator of the run.

        Returns:
            bool: True if the user is the creator, False otherwise.
        """
        run_id = view.kwargs.get("run_id")
        request_user = request.user

        run_filter = Run.objects.filter(pk=run_id)
        if run_filter.exists():
            run_object = run_filter[0]
            if request_user == run_object.creator:
                return True
        return False
