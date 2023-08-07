from django.urls import path

from workflow_settings.views.view_file import FileUploadView
from workflow_settings.views.view_workflow import WorkflowView

urlpatterns = [
    path('file_upload/', FileUploadView.as_view(), name='file_upload'),
    path('workflow/', WorkflowView.as_view(), name='workflow'),
]
