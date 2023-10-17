from django.urls import path

from workflow_settings.views.view_file import FileView
from workflow_settings.views.view_labelfunction import LabelfunctionView
from workflow_settings.views.view_run import RunView
from workflow_settings.views.view_workflow import WorkflowView

urlpatterns = [
    # url for upload for the datasets
    path('file_upload/<int:pk>/', FileView.as_view(), name='file_upload'),

    # workflow related urls
    path('workflow/', WorkflowView.as_view({'get': 'list_all_by_user', 'post': 'create'}), name='workflow'),
    path('workflow/<int:pk>/', WorkflowView.as_view({'get': 'get_by_id', 'delete': 'delete_by_id', 'patch': 'update_by_id'}), name='workflow_user'),
    path('workflow/<int:pk>/contributer/', WorkflowView.as_view({'post': 'add_contributer_by_id', 'delete': 'remove_contributer_by_id'}), name='workflow_contibuter'),

    # labelfunction related urls
    path('workflow/<int:pk>/labelfunction/', LabelfunctionView.as_view({'post': 'add_labelfunction',
                                                                       'get': 'get_all_labelfunction_by_workflow_id',
                                                                       'delete': 'delete_labelfunction',
                                                                       'patch': 'update_labelfunction'}), name='labelfunction'),
    path('workflow/labelfunction/compile/', LabelfunctionView.as_view({'post': 'compile_labelfunction'}), name='labelfunction_compile'),
    path('workflow/labelfunction/test/', LabelfunctionView.as_view({'post': 'test_labelfunction'}), name='labelfunction_test'),

    # run related urls
    path('workflow/<int:pk>/run/', RunView.as_view({'post': 'create_run', 'get': 'get_run'}), name='run'),
    path('workflow/<int:pk>/run/list/', RunView.as_view({'get': 'list_run'}), name='list_run'),
    path('workflow/<int:pk>/run/exec/', RunView.as_view({'get': 'exec_run'}), name='run_exec'),

]
