"""
URL configuration for the labelfunction component.

Path descriptions:
- 'workflow/<int:workflow_id>/': Includes POST and GET for creating a labelfunction and listing all
                                 of the workflow's labelfunctions
- 'workflow/<int:workflow_id>/<str:type>/': Includes PATCH and GET to changing and
                                            returning a specific label or import declaration.
- '<int:labelfunction_id>/modifiy/': Includes GET for deleting, updating
                                     and accessing a labelfunction.
"""

from django.urls import path

from workflow_settings.views.view_labelfunktion.view_labelfunction import (
    LabelfunctionView,
    LabelfunctionModifyView,
)

urlpatterns = [
    path(
        "workflow/<int:workflow_id>/",
        LabelfunctionView.as_view(
            {"post": "add_labelfunction", "get": "get_all_labelfunction_by_workflow_id"}
        ),
        name="labelfunction",
    ),
    path(
        "workflow/<int:workflow_id>/<str:type>/",
        LabelfunctionView.as_view(
            {"get": "get_import_labels", "patch": "update_import_labels"}
        ),
        name="labelfunction_imports",
    ),
    path(
        "<int:labelfunction_id>/modifiy/",
        LabelfunctionModifyView.as_view(
            {
                "get": "get_labelfunction_by_id",
                "delete": "delete_labelfunction",
                "patch": "update_labelfunction",
            }
        ),
        name="labelfunction_id",
    ),
]
