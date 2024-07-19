"""
URL configuration for the run component.

Path descriptions:
- '<int:workflow_id>/create/': Includes POST and GET for creating a run and listing all
                               of the user's runs
- '<int:run_id>/': Includes PUT and GET to change a run and return a specific run of a user.
- '<int:run_id>/exec/': Includes GET for executing a run.
- '<int:run_id>/runaccess/': Includes GET for an authorisation query for a run.
- '<int:run_id>/trainclassifier/': Includes POST for summarising annotations, feature generation and
                                   training a classifier.
"""

from django.urls import path

from workflow_settings.views.view_run.view_classifier import ClassiferView
from workflow_settings.views.view_run.view_run import (
    RunCreateView,
    RunView,
    RunAuthenticateView,
)

urlpatterns = [
    # run related urls
    path(
        "<int:workflow_id>/create/",
        RunCreateView.as_view({"post": "create_run", "get": "list_run"}),
        name="create_run",
    ),
    path(
        "<int:run_id>/",
        RunView.as_view({"put": "update_run", "get": "get_run_by_id"}),
        name="run",
    ),
    path("<int:run_id>/exec/", RunView.as_view({"get": "exec_run"}), name="run_exec"),
    path(
        "<int:run_id>/runaccess/",
        RunAuthenticateView.as_view({"get": "get_access"}),
        name="access_run",
    ),
    # classifier
    path(
        "<int:run_id>/trainclassifier/",
        ClassiferView.as_view({"post": "call_classifier"}),
        name="naive_bayes",
    ),
]
