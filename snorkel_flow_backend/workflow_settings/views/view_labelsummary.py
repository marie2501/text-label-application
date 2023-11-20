import json
import sys

from snorkel.labeling import labeling_function, PandasLFApplier, LFAnalysis
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from snorkel.labeling.model import MajorityLabelVoter
import numpy as np
from snorkel.labeling.model import LabelModel


from rest_framework import status, authentication, viewsets
from rest_framework.parsers import JSONParser, FileUploadParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import HttpResponseForbidden, HttpResponseNotFound, HttpResponseBadRequest

from snorkel_flow_backend.settings import MEDIA_ROOT
from workflow_settings.models import Labelfunction, Workflow, File, Feature, Run, LabelSummary
from workflow_settings.serializers.serializers_labelfunction import LabelfunctionSerializer, LabelfunctionCreateSerializer


class LabelView(viewsets.ViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated]
    parser_class = [JSONParser]

    def getLabelModel(self, request, *args, **kwargs):
        run_id = kwargs['pk']
        run = Run.objects.filter(pk=run_id)
        if run.exists():
            run = run[0]
            if run.labelsummary.objects.exists():
                data = {'type': run.labelsummary.type}
                return Response(data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)


    def majority_vote(self, request, *args, **kwargs):
        run_id = kwargs['pk']
        run = Run.objects.filter(pk=run_id)
        if run.exists():
            run = run[0]
            majority_model = MajorityLabelVoter()
            labelmatrix_json = json.loads(run.labelmatrix)
            labelmatrix = np.array(labelmatrix_json)
            preds_unlabeled = majority_model.predict(L=labelmatrix)
            preds_unlabeled_json = json.dumps(preds_unlabeled.tolist())

            label = LabelSummary.objects.get_or_create(type='M', label_summary=preds_unlabeled_json)
            run.labelsummary = label[0]
            run.save()

            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)


    def label_model(self, request, *args, **kwargs):
        run_id = kwargs['pk']
        # todo speichere cardinality mit in der datenbank, n_epochs... selber wählen -> Referenz welche klassen es gibt
        run = Run.objects.filter(pk=run_id)
        if run.exists():
            run = run[0]
            label_model = LabelModel(cardinality=2, verbose=True)
            labelmatrix_json = json.loads(run.labelmatrix)
            labelmatrix = np.array(labelmatrix_json)
            label_model.fit(L_train=labelmatrix, n_epochs=500, log_freq=100, seed=123)
            preds_unlabeled = label_model.predict(L=labelmatrix)
            preds_unlabeled_json = json.dumps(preds_unlabeled.tolist())

            label = LabelSummary.objects.get_or_create(type='P', label_summary=preds_unlabeled_json)
            run.labelsummary = label[0]
            run.save()

            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)