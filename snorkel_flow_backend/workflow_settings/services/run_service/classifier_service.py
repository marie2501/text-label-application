import json

import pandas as pd
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from rest_framework import status
# import joblib

from snorkel_flow_backend.settings import MEDIA_ROOT
from workflow_settings.models import File, Run, Classifier
from workflow_settings.services.run_service.feature_generation_service import FeatureGenerationService
from workflow_settings.services.run_service.labelmodel_service import LabelModelService


class ClassiferService:

    # todo get classifier assocatied with the run, make model to download
# todo füge im file object noch die anzahl der cardinality zu, am besten so das dieses automatisch berechnet wird
    def call_classifier(self, run_id, selectedModelClassifier, selectedModelLabel, selectedModelFeaturize, range_x,
                        range_y, n_epochs, log_freq, seed, base_learning_rate, l2, numbers_of_labels):
        run_filter = Run.objects.filter(pk=run_id)

        if run_filter.exists():
            run_object = run_filter[0]

            # get dataset file
            workflow_id = run_object.workflow.id
            file = File.objects.filter(workflow_id=workflow_id)
            file_name = file[0].__str__()
            file_path = "{root}/{name}".format(root=MEDIA_ROOT, name=file_name)

            dataframe = pd.read_csv(file_path)

            text_list_test, text_list_test_class, text_list_train, text_list_train_class, text_list_unlabeled = self.extract_col_from_dataframe(
                dataframe)

            # 1. Labelmodel
            preds_unlabeled = self.__call_label_modell(base_learning_rate, l2, log_freq, n_epochs, numbers_of_labels,
                                                     run_object, seed, selectedModelLabel)


            # 2. Featurize
            features_test, features_train, features_unlabeled = self.__call_feature_generation(range_x, range_y,
                                                                                             run_object,
                                                                                             selectedModelFeaturize,
                                                                                             text_list_test,
                                                                                             text_list_train,
                                                                                             text_list_unlabeled)
            # 3. Classifier
            score_test, score_train, model = 0, 0, None
            if selectedModelClassifier == 'Naive Bayes':
                score_test, score_train, model, predictions_train = self.__classifier_naive_bayes(features_test, features_train, features_unlabeled,
                                                                  preds_unlabeled, run_object, text_list_test_class,
                                                                  text_list_train_class)
            elif selectedModelClassifier == 'Decision Tree':
                score_test, score_train, model, predictions_train = self.__classifier_decision_tree(features_test, features_train, features_unlabeled,
                                                                  preds_unlabeled, run_object, text_list_test_class,
                                                                  text_list_train_class)
            elif selectedModelClassifier == 'Random Forest':
                score_test, score_train, model, predictions_train = self.__classifier_random_forest(features_test, features_train, features_unlabeled,
                                                                  preds_unlabeled, run_object, text_list_test_class,
                                                                  text_list_train_class)
            elif selectedModelClassifier == 'KNeighbors':
                score_test, score_train, model, predictions_train = self.__classifier_kneighbors(features_test, features_train, features_unlabeled,
                                                                  preds_unlabeled, run_object, text_list_test_class,
                                                                  text_list_train_class)
            elif selectedModelClassifier == 'Logistic Regression':
                score_test, score_train, model, predictions_train = self.__classifier_logistic_regression(features_test, features_train, features_unlabeled,
                                                                  preds_unlabeled, run_object, text_list_test_class,
                                                                  text_list_train_class)

            return status.HTTP_200_OK, {'score_train': score_train, 'score_test': score_test}, predictions_train

        return status.HTTP_404_NOT_FOUND, {"message": "The run object does not exist"}

    def extract_col_from_dataframe(self, dataframe):
        dataframe_unlabeled = dataframe.loc[(dataframe['splitting_id'] == 'unlabeled')]
        dataframe_train = dataframe.loc[(dataframe['splitting_id'] == 'train')]
        dataframe_test = dataframe.loc[(dataframe['splitting_id'] == 'test')]
        text_list_unlabeled = dataframe_unlabeled['text'].tolist()
        text_list_train = dataframe_train['text'].tolist()
        text_list_test = dataframe_test['text'].tolist()
        text_list_train_class = dataframe_train['CLASS'].tolist()
        text_list_test_class = dataframe_test['CLASS'].tolist()
        return text_list_test, text_list_test_class, text_list_train, text_list_train_class, text_list_unlabeled

    def __classifier_naive_bayes(self, features_test, features_train, features_unlabeled, preds_unlabeled, run_object,
                               text_list_test_class, text_list_train_class):
        clf = MultinomialNB()
        clf.fit(features_unlabeled, preds_unlabeled)
        score_train = clf.score(features_train, text_list_train_class)
        predictions_train = clf.predict(features_train)
        score_test = clf.score(features_test, text_list_test_class)
        classifier = Classifier.objects.get_or_create(type='NB', test_score=score_test, train_score=score_train)
        run_object.classifier = classifier[0]
        run_object.save()
        return score_test, score_train, clf, predictions_train


    def __classifier_random_forest(self, features_test, features_train, features_unlabeled, preds_unlabeled, run_object,
                               text_list_test_class, text_list_train_class):
        clf = RandomForestClassifier()
        clf.fit(features_unlabeled, preds_unlabeled)
        score_train = clf.score(features_train, text_list_train_class)
        predictions_train = clf.predict(features_train)
        score_test = clf.score(features_test, text_list_test_class)
        classifier = Classifier.objects.get_or_create(type='RF', test_score=score_test, train_score=score_train)
        run_object.classifier = classifier[0]
        run_object.save()
        return score_test, score_train, clf, predictions_train

    def __classifier_decision_tree(self, features_test, features_train, features_unlabeled, preds_unlabeled, run_object,
                               text_list_test_class, text_list_train_class):
        clf = DecisionTreeClassifier()
        clf.fit(features_unlabeled, preds_unlabeled)
        score_train = clf.score(features_train, text_list_train_class)
        predictions_train = clf.predict(features_train)
        score_test = clf.score(features_test, text_list_test_class)
        classifier = Classifier.objects.get_or_create(type='DT', test_score=score_test, train_score=score_train)
        run_object.classifier = classifier[0]
        run_object.save()
        return score_test, score_train, clf, predictions_train

    def __classifier_kneighbors(self, features_test, features_train, features_unlabeled, preds_unlabeled, run_object,
                               text_list_test_class, text_list_train_class):
        clf = KNeighborsClassifier(n_neighbors=5)
        clf.fit(features_unlabeled, preds_unlabeled)
        score_train = clf.score(features_train, text_list_train_class)
        predictions_train = clf.predict(features_train)
        score_test = clf.score(features_test, text_list_test_class)
        classifier = Classifier.objects.get_or_create(type='KN', test_score=score_test, train_score=score_train)
        run_object.classifier = classifier[0]
        run_object.save()
        return score_test, score_train, clf, predictions_train

    def __classifier_logistic_regression(self, features_test, features_train, features_unlabeled, preds_unlabeled, run_object,
                               text_list_test_class, text_list_train_class):
        clf = LogisticRegression()
        clf.fit(features_unlabeled, preds_unlabeled)
        score_train = clf.score(features_train, text_list_train_class)
        predictions_train = clf.predict(features_train)
        score_test = clf.score(features_test, text_list_test_class)
        classifier = Classifier.objects.get_or_create(type='LR', test_score=score_test, train_score=score_train)
        run_object.classifier = classifier[0]
        run_object.save()
        return score_test, score_train, clf, predictions_train

    def __call_feature_generation(self, range_x, range_y, run_object, selectedModelFeaturize, text_list_test,
                                text_list_train, text_list_unlabeled):
        featuregenerationservice = FeatureGenerationService()
        features_test, features_train, features_unlabeled = featuregenerationservice.extraxt_features(range_x, range_y,
                                                                                                      selectedModelFeaturize,
                                                                                                      text_list_test,
                                                                                                      text_list_train,
                                                                                                      text_list_unlabeled,
                                                                                                      run_object)
        return features_test, features_train, features_unlabeled

    def __call_label_modell(self, base_learning_rate, l2, log_freq, n_epochs, numbers_of_labels, run_object, seed,
                          selectedModelLabel):
        labelmodelservice = LabelModelService()
        preds_unlabeled = labelmodelservice.label_model(run_object, selectedModelLabel, n_epochs, log_freq, seed,
                                                        base_learning_rate, l2, numbers_of_labels)
        run_object.preds_unlabeled = json.dumps(preds_unlabeled.tolist())
        run_object.save()
        return preds_unlabeled





