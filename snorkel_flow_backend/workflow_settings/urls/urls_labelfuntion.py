from django.urls import path

from workflow_settings.views.view_classifier import ClassiferView
from workflow_settings.views.view_labelfunction import LabelfunctionView
from workflow_settings.views.view_run import RunView

urlpatterns = [

    # labelfunction related urls
    path('workflow/<int:pk>/labelfunction/', LabelfunctionView.as_view({'post': 'add_labelfunction',
                                                                       'get': 'get_all_labelfunction_by_workflow_id',
                                                                       'delete': 'delete_labelfunction',
                                                                       'patch': 'update_labelfunction'}), name='labelfunction'),
    path('workflow/labelfunction/<int:pk>/compile/', LabelfunctionView.as_view({'post': 'compile_labelfunction'}), name='labelfunction_compile'),
    path('workflow/<int:pk>/labelfunction/test/', LabelfunctionView.as_view({'post': 'test_labelfunction'}), name='labelfunction_test'),
    path('workflow/<int:pk>/labelfunction/import/', LabelfunctionView.as_view({'get': 'get_imports'}), name='labelfunction_imports'),
    path('workflow/labelfunction/<int:pk>/', LabelfunctionView.as_view({'get': 'get_labelfunction_by_id'}), name='labelfunction_id'),

    # run related urls
    path('workflow/<int:pk>/run/', RunView.as_view({'post': 'create_run','put': 'update_run', 'get': 'get_run'}), name='run'),
    path('workflow/<int:pk>/run/list/', RunView.as_view({'get': 'list_run'}), name='list_run'),
    path('workflow/<int:pk>/run/exec/', RunView.as_view({'get': 'exec_run'}), name='run_exec'),
    path('workflow/<int:pk>/run/analysis/', RunView.as_view({'get': 'get_analysis'}), name='run_analysis'),

    # classifier
    path('workflow/run/<int:pk>/naivebayes/', ClassiferView.as_view({'post': 'naive_bayes'}), name='naive_bayes'),

]
