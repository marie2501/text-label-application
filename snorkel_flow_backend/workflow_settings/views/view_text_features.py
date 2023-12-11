import json
import sys

from snorkel.labeling import labeling_function, PandasLFApplier, LFAnalysis
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer


from rest_framework import status, authentication, viewsets
from rest_framework.parsers import JSONParser, FileUploadParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import HttpResponseForbidden, HttpResponseNotFound, HttpResponseBadRequest

from snorkel_flow_backend.settings import MEDIA_ROOT
from workflow_settings.models import Labelfunction, Workflow, File, Feature, Run
from workflow_settings.serializers.serializers_labelfunction import LabelfunctionSerializer, LabelfunctionCreateSerializer


class TextFeatureView(viewsets.ViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated]
    parser_class = [JSONParser]

    # todo get text feaute assoiatet with the run



