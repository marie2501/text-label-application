"""
URL configuration for the file component.

Path descriptions:
- '<int:workflow_id>/': Includes POST, PUT and GET for uploading, updating or getting
                        the existence of a file in a workflow.
- 'download/<int:run_id>/file/': Includes GET for downloading an annotated data set.
"""

from django.urls import path

from workflow_settings.views.view_file.view_file_upload import FileUploadView
from workflow_settings.views.view_file.view_file_download import FileDownloadView

urlpatterns = [
    path("<int:workflow_id>/", FileUploadView.as_view(), name="file_upload"),
    path("download/<int:run_id>/file/", FileDownloadView.as_view(), name="file_download"),
]
