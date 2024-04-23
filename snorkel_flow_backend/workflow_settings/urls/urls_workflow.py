from django.urls import path

from workflow_settings.views.view_workflow_setting.view_contributer import ContributerModifyView, ContributerView
from workflow_settings.views.view_workflow_setting.view_workflow import WorkflowView, WorkflowAuthenticatetOnlyView, \
    WorkflowModifyView

urlpatterns = [

    # workflow related urls
    path('', WorkflowAuthenticatetOnlyView.as_view({'get': 'list_all_by_user', 'post': 'create'}), name='workflow'),
    path('package/', WorkflowAuthenticatetOnlyView.as_view({'get': 'get_installed_packages'}), name='package'),
    path('<int:workflow_id>/', WorkflowView.as_view({'get': 'get_by_id'}), name='workflow_user'),
    path('<int:workflow_id>/', WorkflowModifyView.as_view({'delete': 'delete_by_id', 'patch': 'update_by_id'}), name='workflow_modify'),

    path('<int:workflow_id>/isCreator/', WorkflowView.as_view({'get': 'user_is_workflow_creator'}), name='workflow_creator'),

    path('<int:workflow_id>/contributer/modify/', ContributerModifyView.as_view(
        {'get': 'filter_contributers', 'post': 'add_contributer_by_id', 'delete': 'remove_contributer_by_id'}),
         name='contibuter_modify'),
    path('<int:workflow_id>/contributer/', ContributerView.as_view(
        {'get': 'get_contributers'}),
         name='contibuter'),

]
