import json

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

from snorkel_flow_backend.settings import MEDIA_ROOT
from workflow_settings.models import Labelfunction, Workflow, File, Feature, Run, LabelSummary, Classifier


class ClassiferView(viewsets.ViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated]
    parser_class = [JSONParser]

    # todo get classifier assocatied with the run

    def naive_bayes(self, request, *args, **kwargs):
        run_id = kwargs['pk']
        run = Run.objects.filter(pk=run_id)
        selectedModelClassifier = request.data['selectedModelClassifier']
        selectedModelLabel = request.data['selectedModelLabel']
        selectedModelFeaturize = request.data['selectedModelFeaturize']
        range_x = request.data['range_x']
        range_y = request.data['range_y']
        if run.exists():
            run = run[0]

            # get dataset file
            workflow_id = run.workflow.id
            file = File.objects.filter(workflow_id=workflow_id)
            file_name = file[0].__str__()
            file_path = "{root}/{name}".format(root=MEDIA_ROOT, name=file_name)

            dataframe = pd.read_csv(file_path)

            # 1. Labelmodel
            preds_unlabeled = self.train_label_model(run, selectedModelLabel)

            # 2. Featurize
            dataframe_unlabeled = dataframe.loc[(dataframe['splitting_id'] == 'unlabeled')]
            dataframe_train = dataframe.loc[(dataframe['splitting_id'] == 'train')]
            dataframe_test = dataframe.loc[(dataframe['splitting_id'] == 'test')]

            text_list_unlabeled = dataframe_unlabeled['text'].tolist()
            text_list_train = dataframe_train['text'].tolist()
            text_list_test = dataframe_test['text'].tolist()

            features_test, features_train, features_unlabeled = self.extraxt_features(range_x, range_y,
                                                                                      selectedModelFeaturize,
                                                                                      text_list_test, text_list_train,
                                                                                      text_list_unlabeled)


            # 3. Classifier
            text_list_train_class = dataframe_train['CLASS'].tolist()
            text_list_test_class = dataframe_test['CLASS'].tolist()

            clf = MultinomialNB()
            clf.fit(features_unlabeled, preds_unlabeled)
            score_train = clf.score(features_train, text_list_train_class)
            score_test = clf.score(features_test, text_list_test_class)

            print(score_train, score_test)

            self.store_run_setting_information(range_x, range_y, run, score_test, score_train, selectedModelClassifier,
                                               selectedModelFeaturize, selectedModelLabel)

            return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_404_NOT_FOUND)

    def store_run_setting_information(self, range_x, range_y, run, score_test, score_train, selectedModelClassifier,
                                      selectedModelFeaturize, selectedModelLabel):
        if selectedModelLabel == 'Majority Vote':
            label = LabelSummary.objects.get_or_create(type='M')
            run.labelsummary = label[0]
            run.save()
        elif selectedModelLabel == 'Train Label Model':
            label = LabelSummary.objects.get_or_create(type='P')
            run.labelsummary = label[0]
            run.save()
        if selectedModelFeaturize == 'Bag of words':
            feature = Feature.objects.get_or_create(range_x=range_x, range_y=range_y, type='BW')
            run.feature = feature[0]
            run.save()
        elif selectedModelFeaturize == 'TFIDF':
            feature = Feature.objects.get_or_create(range_x=range_x, range_y=range_y, type='BW')
            run.feature = feature[0]
            run.save()
        if selectedModelClassifier == 'Naive Bayes':
            classifier = Classifier.objects.get_or_create(type='NB', test_score=score_test, train_score=score_train)
            run.classifier = classifier[0]
            run.save()

    def extraxt_features(self, range_x, range_y, selectedModelFeaturize, text_list_test, text_list_train,
                         text_list_unlabeled):
        if selectedModelFeaturize == 'Bag of words':
            vectorizer = CountVectorizer(ngram_range=(range_x, range_y))
            vectorizer.fit(text_list_unlabeled)
            features_unlabeled = vectorizer.transform(text_list_unlabeled)
            features_train = vectorizer.transform(text_list_train)
            features_test = vectorizer.transform(text_list_test)
            return features_test, features_train, features_unlabeled
        elif selectedModelFeaturize == 'TFIDF':
            vectorizer = TfidfVectorizer()
            vectorizer.fit(text_list_unlabeled)
            features_unlabeled = vectorizer.transform(text_list_unlabeled)
            features_train = vectorizer.transform(text_list_train)
            features_test = vectorizer.transform(text_list_test)
            return features_test, features_train, features_unlabeled

    # todo speichere cardinality mit in der datenbank, n_epochs... selber wählen -> Referenz welche klassen es gibt
    def train_label_model(self, run, selectedModelLabel):
        if selectedModelLabel == 'Majority Vote':
            majority_model = MajorityLabelVoter()
            labelmatrix_json = json.loads(run.labelmatrix)
            labelmatrix = np.array(labelmatrix_json)
            preds_unlabeled = majority_model.predict(L=labelmatrix)
            return preds_unlabeled
        elif selectedModelLabel == 'Train Label Model':
            label_model = LabelModel(cardinality=2, verbose=True)
            labelmatrix_json = json.loads(run.labelmatrix)
            labelmatrix = np.array(labelmatrix_json)
            label_model.fit(L_train=labelmatrix, n_epochs=500, log_freq=100, seed=123)
            preds_unlabeled = label_model.predict(L=labelmatrix)
            return preds_unlabeled
