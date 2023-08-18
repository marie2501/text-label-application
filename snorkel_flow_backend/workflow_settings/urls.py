from django.urls import path

from workflow_settings.views.view_file import FileUploadView
from workflow_settings.views.view_workflow import WorkflowView

urlpatterns = [
    path('file_upload/', FileUploadView.as_view(), name='file_upload'),
    path('workflow/', WorkflowView.as_view({'get': 'list_all_by_user', 'post': 'create'}), name='workflow'),
    path('workflow/<int:pk>/', WorkflowView.as_view({'get': 'get_by_id', 'delete': 'delete_by_id', 'patch': 'update_by_id'}), name='workflow_user'),
    path('workflow/<int:pk>/contributer/', WorkflowView.as_view({'post': 'add_contributer_by_id', 'delete': 'remove_contributer_by_id'}), name='workflow_contibuter'),
]
