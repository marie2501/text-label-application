"""
URL configuration for the workflow component.

Path descriptions:
- '': Includes POST and GET for creating a workflow and listing all
                               of the user's workflows
- 'package/': Includes GET to get the package list.
- '<int:workflow_id>/': Includes GET, DELETE and PATCH for
                        deleting, updating and accessing a workflow.
- '<int:workflow_id>/isCreator/': Includes GET for an authorisation query for a workflow.
- '<int:workflow_id>/access/': Includes GET for an authorisation query for a workflow.
- '<int:workflow_id>/contributer/modify/': Includes GET, POST and DELETE for
                                           searching, deleting and adding a contributor.
- '<int:workflow_id>/contributer/': Includes GET for the list of all contributors.
"""

from django.urls import path

from workflow_settings.views.view_workflow_setting.view_contributer import (
    ContributerModifyView,
    ContributerView,
)
from workflow_settings.views.view_workflow_setting.view_workflow import (
    WorkflowView,
    WorkflowAuthenticatetOnlyView,
    WorkflowModifyView,
)

urlpatterns = [
    # workflow related urls
    path(
        "",
        WorkflowAuthenticatetOnlyView.as_view(
            {"get": "list_all_by_user", "post": "create"}
        ),
        name="workflow",
    ),
    path(
        "package/",
        WorkflowAuthenticatetOnlyView.as_view({"get": "get_installed_packages"}),
        name="package",
    ),
    path(
        "<int:workflow_id>/",
        WorkflowView.as_view({"get": "get_by_id"}),
        name="workflow_user",
    ),
    path(
        "<int:workflow_id>/",
        WorkflowModifyView.as_view({"delete": "delete_by_id", "patch": "update_by_id"}),
        name="workflow_modify",
    ),
    path(
        "<int:workflow_id>/isCreator/",
        WorkflowView.as_view({"get": "user_is_workflow_creator"}),
        name="workflow_creator",
    ),
    path(
        "<int:workflow_id>/access/",
        WorkflowAuthenticatetOnlyView.as_view({"get": "get_access"}),
        name="access_work",
    ),
    # contributer related urls
    path(
        "<int:workflow_id>/contributer/modify/",
        ContributerModifyView.as_view(
            {
                "get": "filter_contributers",
                "post": "add_contributer_by_id",
                "delete": "remove_contributer_by_id",
            }
        ),
        name="contibuter_modify",
    ),
    path(
        "<int:workflow_id>/contributer/",
        ContributerView.as_view({"get": "get_contributers"}),
        name="contibuter",
    ),
]
