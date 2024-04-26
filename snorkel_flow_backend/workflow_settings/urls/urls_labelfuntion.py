from django.urls import path

from workflow_settings.views.view_labelfunktion.view_labelfunction import LabelfunctionView, LabelfunctionModifyView

urlpatterns = [

    path('workflow/<int:workflow_id>/labelfunction/', LabelfunctionView.as_view({'post': 'add_labelfunction',
                                                                       'get': 'get_all_labelfunction_by_workflow_id'}), name='labelfunction'),
    path('workflow/labelfunction/<int:workflow_id>/compile/', LabelfunctionView.as_view({'post': 'compile_labelfunction'}), name='labelfunction_compile'),
    path('workflow/<int:workflow_id>/labelfunction/test/', LabelfunctionView.as_view({'post': 'test_labelfunction'}), name='labelfunction_test'),
    path('workflow/<int:workflow_id>/labelfunction/import/', LabelfunctionView.as_view({'get': 'get_imports', 'patch': 'update_import'}), name='labelfunction_imports'),


    path('workflow/labelfunction/<int:labelfunction_id>/modifiy/', LabelfunctionModifyView.as_view({'get': 'get_labelfunction_by_id', 'delete': 'delete_labelfunction',
                                                                       'patch': 'update_labelfunction'}), name='labelfunction_id'),

]
