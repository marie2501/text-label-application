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


    def bag_of_words_featurization(self, request, *args, **kwargs):
        workflow_id = kwargs['w_pk']
        run_id = kwargs['r_pk']
        range_x = request.data['range_x']
        range_y = request.data['range_y']

        file = File.objects.filter(workflow_id=workflow_id)
        run = Run.objects.filter(pk=run_id)
        if file.exists():
            run = run[0]

            file_name = file[0].__str__()
            file_path = "{root}/{name}".format(root=MEDIA_ROOT, name=file_name)

            dataframe = pd.read_csv(file_path)
            dataframe_unlabeled = dataframe.loc[(dataframe['splitting_id'] == 'unlabeled')]
            dataframe_train = dataframe.loc[(dataframe['splitting_id'] == 'train')]
            dataframe_test = dataframe.loc[(dataframe['splitting_id'] == 'test')]

            text_list_unlabeled = dataframe_unlabeled['text'].tolist()
            text_list_train = dataframe_train['text'].tolist()
            text_list_test = dataframe_test['text'].tolist()
            text_corpus = dataframe['text'].tolist()

            vectorizer = CountVectorizer(ngram_range=(range_x, range_y))
            vectorizer.fit(text_corpus)
            features_unlabeled = vectorizer.transform(text_list_unlabeled)
            features_train = vectorizer.transform(text_list_train)
            features_test = vectorizer.transform(text_list_test)

            features_test_json = json.dumps(features_test.toarray().tolist())
            features_train_json = json.dumps(features_train.toarray().tolist())
            features_unlabeled_json = json.dumps(features_unlabeled.toarray().tolist())

            feature = Feature.objects.get_or_create(range_x=range_x, range_y=range_y, type='BW',
                                          features_train=features_train_json,
                                          features_test=features_test_json, features_unlabeled=features_unlabeled_json)

            run.feature = feature[0]
            run.save()

            return Response(status=status.HTTP_200_OK)


    def tfidf_featurization(self, request, *args, **kwargs):
        workflow_id = kwargs['w_pk']
        run_id = kwargs['r_pk']
        range_x = request.data['range_x']
        range_y = request.data['range_y']

        file = File.objects.filter(workflow_id=workflow_id)
        run = Run.objects.filter(pk=run_id)
        if file.exists():
            run = run[0]

            file_name = file[0].__str__()
            file_path = "{root}/{name}".format(root=MEDIA_ROOT, name=file_name)

            dataframe = pd.read_csv(file_path)
            dataframe_unlabeled = dataframe.loc[(dataframe['splitting_id'] == 'unlabeled')]
            dataframe_train = dataframe.loc[(dataframe['splitting_id'] == 'train')]
            dataframe_test = dataframe.loc[(dataframe['splitting_id'] == 'test')]

            text_list_unlabeled = dataframe_unlabeled['text'].tolist()
            text_list_train = dataframe_train['text'].tolist()
            text_list_test = dataframe_test['text'].tolist()
            text_corpus = dataframe['text'].tolist()

            vectorizer = TfidfVectorizer()
            vectorizer.fit(text_corpus)
            features_unlabeled = vectorizer.transform(text_list_unlabeled)
            features_train = vectorizer.transform(text_list_train)
            features_test = vectorizer.transform(text_list_test)

            features_test_json = json.dumps(features_test.toarray().tolist())
            features_train_json = json.dumps(features_train.toarray().tolist())
            features_unlabeled_json = json.dumps(features_unlabeled.toarray().tolist())

            feature = Feature.objects.get_or_create(range_x=range_x, range_y=range_y, type='TF', features_train=features_train_json,
                                          features_test=features_test_json, features_unlabeled=features_unlabeled_json)

            run.feature = feature[0]
            run.save()

            return Response(status=status.HTTP_200_OK)



