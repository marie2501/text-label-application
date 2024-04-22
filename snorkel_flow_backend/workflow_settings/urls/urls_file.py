from django.urls import path

from workflow_settings.views.view_file.view_file_upload import FileUploadView
from workflow_settings.views.view_file.view_file_download import FileDownloadView

urlpatterns = [

    path('<int:workflow_id>/', FileUploadView.as_view(), name='file_upload'),
    path('download/<int:run_id>/', FileDownloadView.as_view(), name='file_download'),

]
