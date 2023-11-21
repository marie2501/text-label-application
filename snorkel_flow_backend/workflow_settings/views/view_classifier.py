import json
import sys

from snorkel.labeling import labeling_function, PandasLFApplier, LFAnalysis
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
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
from workflow_settings.serializers.serializers_labelfunction import LabelfunctionSerializer, \
    LabelfunctionCreateSerializer


class ClassiferView(viewsets.ViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated]
    parser_class = [JSONParser]

    def naive_bayes(self, request, *args, **kwargs):
        run_id = kwargs['pk']
        run = Run.objects.filter(pk=run_id)
        if run.exists():
            run = run[0]

            workflow_id = run.workflow.id
            file = File.objects.filter(workflow_id=workflow_id)
            file_name = file[0].__str__()
            file_path = "{root}/{name}".format(root=MEDIA_ROOT, name=file_name)

            dataframe = pd.read_csv(file_path)

            dataframe_train = dataframe.loc[(dataframe['splitting_id'] == 'train')]
            dataframe_test = dataframe.loc[(dataframe['splitting_id'] == 'test')]
            text_list_train_class = dataframe_train['CLASS'].tolist()
            text_list_test_class = dataframe_test['CLASS'].tolist()

            feature_unlabeled = np.array(json.loads(run.feature.features_unlabeled))
            feature_unlabeled_erg = np.array(json.loads(run.labelsummary.label_summary))

            feature_train = np.array(json.loads(run.feature.features_train))

            feature_test = np.array(json.loads(run.feature.features_test))

            clf = MultinomialNB()

            clf.fit(feature_unlabeled, feature_unlabeled_erg)

            score = clf.score(feature_train, text_list_train_class)

            print(score)

            return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_404_NOT_FOUND)
