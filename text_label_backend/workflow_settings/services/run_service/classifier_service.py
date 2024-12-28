"""
classifier_service.py

This module provides the functionalities to train a classifier.

Classes:
- ClassiferService
"""
import json

import pandas as pd
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from rest_framework import status

from text_label_backend.settings import MEDIA_ROOT
from workflow_settings.models import File, Run, Classifier
from workflow_settings.services.run_service.feature_generation_service import (
    FeatureGenerationService,
)
from workflow_settings.services.run_service.labelmodel_service import LabelModelService


class ClassiferService:
    """
    Service class to train a classifier.

    Methods:
    - call_classifier(
        self, run_id, selectedModelClassifier, selectedModelLabel, selectedModelFeaturize,
        range_x, range_y, n_epochs, log_freq, seed, base_learning_rate, l2, numbers_of_labels,
        selectedTie, filterAbstain
      )
        Calls a labelmodel, a feature generation method and a classifier
    - extract_col_from_dataframe(self, dataframe):
        Returns the texts and class values of the dataset.
    - __classifier_naive_bayes(self, features_test, features_train, features_unlabeled, preds_unlabeled,
                               run_object, text_list_test_class, text_list_train_class):
        Applyies the Naive Bayses Classifier.
    - __classifier_random_forest(self, features_test, features_train, features_unlabeled, preds_unlabeled,
                                 run_object, text_list_test_class, text_list_train_class):
        Applyies the Random Forest Classifier.
    - __classifier_decision_tree(self, features_test, features_train, features_unlabeled, preds_unlabeled,
                                 run_object, text_list_test_class, text_list_train_class)
        Applyies the decision tree Classifier.
    - __classifier_kneighbors(self, features_test, features_train, features_unlabeled, preds_unlabeled,
                              run_object, text_list_test_class, text_list_train_class):
        Applyies the kneighbors Classifier.
    - __classifier_logistic_regression(self, features_test, features_train, features_unlabeled, preds_unlabeled,
                                       run_object, text_list_test_class, text_list_train_class):
        Applyies the logistic regression Classifier.
    - __call_feature_generation(self, range_x, range_y, run_object, selectedModelFeaturize, text_list_test,
                                text_list_train, text_list_unlabeled):
        Applyies the feature generation.
    - __call_label_modell(self, base_learning_rate, l2, log_freq, n_epochs, numbers_of_labels, run_object,
                          seed, selectedModelLabel, selectedTie):
        Applyies the Labelmodel.
    - __filter_abstain_in_dataset(self, text_list_unlabeled, preds_unlabeled, filterAbstain):
        Filters the Abstains out of the dataset.
    """

    # todo füge im file object noch die anzahl der cardinality zu, am besten so das dieses automatisch berechnet wird
    def call_classifier(
        self,
        run_id,
        selectedModelClassifier,
        selectedModelLabel,
        selectedModelFeaturize,
        range_x,
        range_y,
        n_epochs,
        log_freq,
        seed,
        base_learning_rate,
        l2,
        numbers_of_labels,
        selectedTie,
        filterAbstain,
    ):
        """
        Calls the labelmodel, feature generation and the classifier.

        Args:
            run_id (int): The ID of the run.
            selectedModelClassifier (str): The classifier model to be used ("Naive Bayes", "Decision Tree",
                                           "Random Forest", "KNeighbors", "Logistic Regression").
            selectedModelLabel (str): The labelmodel to be used.
            selectedModelFeaturize (str): The feature extraction model to be applied ("Bag of words" or "TFIDF").
            range_x (int): The lower boundary of the range for n-grams.
            range_y (int): The upper boundary of the range for n-grams.
            n_epochs (int): The number of epochs for training the labelmodel.
            log_freq (int): The log frequency.
            seed (int): The random seed for reproducibility.
            base_learning_rate (float): The base learning rate for the labelmodel.
            l2 (float): The L2 regularization parameter.
            numbers_of_labels (int): The number of labels.
            selectedTie (bool): The option how to handle tie cases in labelmodel.
            filterAbstain (bool): The option to filter out abstained labels.

        Returns:
            - int: A HTTP status code.
            - dict: The scores of the test and training dataset.
            - dict: The classifier and labelfunction predictions of the train dataset
            - error: A dictionary containing an error message
        """
        run_filter = Run.objects.filter(pk=run_id)

        if run_filter.exists():
            run_object = run_filter[0]

            # get dataset file
            workflow_id = run_object.workflow.id
            file = File.objects.filter(workflow_id=workflow_id)
            file_name = file[0].__str__()
            file_path = "{root}/{name}".format(root=MEDIA_ROOT, name=file_name)

            dataframe = pd.read_csv(file_path)

            (
                text_list_test,
                text_list_test_class,
                text_list_train,
                text_list_train_class,
                text_list_unlabeled,
            ) = self.extract_col_from_dataframe(dataframe)

            # 1. Labelmodel
            preds_unlabeled = self.__call_label_modell(
                base_learning_rate,
                l2,
                log_freq,
                n_epochs,
                numbers_of_labels,
                run_object,
                seed,
                selectedModelLabel,
                selectedTie,
            )

            text_list_unlabeled, preds_unlabeled = self.__filter_abstain_in_dataset(
                text_list_unlabeled, preds_unlabeled, filterAbstain
            )

            # 2. Featurize
            features_test, features_train, features_unlabeled = (
                self.__call_feature_generation(
                    range_x,
                    range_y,
                    run_object,
                    selectedModelFeaturize,
                    text_list_test,
                    text_list_train,
                    text_list_unlabeled,
                )
            )

            # 3. Classifier
            score_test, score_train, model, predictions_train = 0, 0, None, None
            if selectedModelClassifier == "Naive Bayes":
                score_test, score_train, model, predictions_train = (
                    self.__classifier_naive_bayes(
                        features_test,
                        features_train,
                        features_unlabeled,
                        preds_unlabeled,
                        run_object,
                        text_list_test_class,
                        text_list_train_class,
                    )
                )
            elif selectedModelClassifier == "Decision Tree":
                score_test, score_train, model, predictions_train = (
                    self.__classifier_decision_tree(
                        features_test,
                        features_train,
                        features_unlabeled,
                        preds_unlabeled,
                        run_object,
                        text_list_test_class,
                        text_list_train_class,
                    )
                )
            elif selectedModelClassifier == "Random Forest":
                score_test, score_train, model, predictions_train = (
                    self.__classifier_random_forest(
                        features_test,
                        features_train,
                        features_unlabeled,
                        preds_unlabeled,
                        run_object,
                        text_list_test_class,
                        text_list_train_class,
                    )
                )
            elif selectedModelClassifier == "KNeighbors":
                score_test, score_train, model, predictions_train = (
                    self.__classifier_kneighbors(
                        features_test,
                        features_train,
                        features_unlabeled,
                        preds_unlabeled,
                        run_object,
                        text_list_test_class,
                        text_list_train_class,
                    )
                )
            elif selectedModelClassifier == "Logistic Regression":
                score_test, score_train, model, predictions_train = (
                    self.__classifier_logistic_regression(
                        features_test,
                        features_train,
                        features_unlabeled,
                        preds_unlabeled,
                        run_object,
                        text_list_test_class,
                        text_list_train_class,
                    )
                )

            return (
                status.HTTP_200_OK,
                {"score_train": score_train, "score_test": score_test},
                predictions_train,
            )

        return status.HTTP_404_NOT_FOUND, {"message": "The run object does not exist"}

    def extract_col_from_dataframe(self, dataframe):
        """
        Extracts text and class columns from the dataframe in list format.

        Args:
            dataframe (DataFrame): The dataframe containing the dataset.

        Returns:
            list: The texts of the test dataset.
            list: The class values of the test dataset.
            list: The texts of the train dataset.
            list: The class values of the test dataset.
            list: The texts of the unlabeled dataset.
        """
        dataframe_unlabeled = dataframe.loc[(dataframe["splitting_id"] == "unlabeled")]
        dataframe_train = dataframe.loc[(dataframe["splitting_id"] == "train")]
        dataframe_test = dataframe.loc[(dataframe["splitting_id"] == "test")]
        text_list_unlabeled = dataframe_unlabeled["text"].tolist()
        text_list_train = dataframe_train["text"].tolist()
        text_list_test = dataframe_test["text"].tolist()
        text_list_train_class = dataframe_train["class"].tolist()
        text_list_test_class = dataframe_test["class"].tolist()
        return (
            text_list_test,
            text_list_test_class,
            text_list_train,
            text_list_train_class,
            text_list_unlabeled,
        )

    def __classifier_naive_bayes(
        self,
        features_test,
        features_train,
        features_unlabeled,
        preds_unlabeled,
        run_object,
        text_list_test_class,
        text_list_train_class,
    ):
        """
        Trains and evaluates a Naive Bayes classifier.

        Args:
            features_test (sparse matrix): The feature matrix for the test data.
            features_train (sparse matrix): The feature matrix for the train data.
            features_unlabeled (sparse matrix): The feature matrix for the unlabeled data.
            preds_unlabeled (array): The predicted labels for the unlabeled data.
            run_object (Run): The run object.
            text_list_test_class (list): The actual labels for the test data.
            text_list_train_class (list): The actual labels for the train data.

        Returns:
            float: The score (accuracy) of the test dataset.
            float: The score (accuracy) of the train dataset.
            classifier: The classifier model
            number: The predictions of the classifier on the train dataset
        """
        clf = MultinomialNB()
        clf.fit(features_unlabeled, preds_unlabeled)
        score_train = clf.score(features_train, text_list_train_class)
        predictions_train = clf.predict(features_train)
        score_test = clf.score(features_test, text_list_test_class)
        classifier = Classifier.objects.get_or_create(
            type="NB", test_score=score_test, train_score=score_train
        )
        run_object.classifier = classifier[0]
        run_object.save()
        return score_test, score_train, clf, predictions_train

    def __classifier_random_forest(
        self,
        features_test,
        features_train,
        features_unlabeled,
        preds_unlabeled,
        run_object,
        text_list_test_class,
        text_list_train_class,
    ):
        """
        Trains and evaluates a Random Forrest classifier.

        Args:
            features_test (sparse matrix): The feature matrix for the test data.
            features_train (sparse matrix): The feature matrix for the train data.
            features_unlabeled (sparse matrix): The feature matrix for the unlabeled data.
            preds_unlabeled (array): The predicted labels for the unlabeled data.
            run_object (Run): The run object.
            text_list_test_class (list): The actual labels for the test data.
            text_list_train_class (list): The actual labels for the train data.

        Returns:
            float: The score (accuracy) of the test dataset.
            float: The score (accuracy) of the train dataset.
            classifier: The classifier model
            number: The predictions of the classifier on the train dataset
        """
        clf = RandomForestClassifier()
        clf.fit(features_unlabeled, preds_unlabeled)
        score_train = clf.score(features_train, text_list_train_class)
        predictions_train = clf.predict(features_train)
        score_test = clf.score(features_test, text_list_test_class)
        classifier = Classifier.objects.get_or_create(
            type="RF", test_score=score_test, train_score=score_train
        )
        run_object.classifier = classifier[0]
        run_object.save()
        return score_test, score_train, clf, predictions_train

    def __classifier_decision_tree(
        self,
        features_test,
        features_train,
        features_unlabeled,
        preds_unlabeled,
        run_object,
        text_list_test_class,
        text_list_train_class,
    ):
        """
        Trains and evaluates a Decision Tree classifier.

        Args:
            features_test (sparse matrix): The feature matrix for the test data.
            features_train (sparse matrix): The feature matrix for the train data.
            features_unlabeled (sparse matrix): The feature matrix for the unlabeled data.
            preds_unlabeled (array): The predicted labels for the unlabeled data.
            run_object (Run): The run object.
            text_list_test_class (list): The actual labels for the test data.
            text_list_train_class (list): The actual labels for the train data.

        Returns:
            float: The score (accuracy) of the test dataset.
            float: The score (accuracy) of the train dataset.
            classifier: The classifier model
            number: The predictions of the classifier on the train dataset
        """
        clf = DecisionTreeClassifier()
        clf.fit(features_unlabeled, preds_unlabeled)
        score_train = clf.score(features_train, text_list_train_class)
        predictions_train = clf.predict(features_train)
        score_test = clf.score(features_test, text_list_test_class)
        classifier = Classifier.objects.get_or_create(
            type="DT", test_score=score_test, train_score=score_train
        )
        run_object.classifier = classifier[0]
        run_object.save()
        return score_test, score_train, clf, predictions_train

    def __classifier_kneighbors(
        self,
        features_test,
        features_train,
        features_unlabeled,
        preds_unlabeled,
        run_object,
        text_list_test_class,
        text_list_train_class,
    ):
        """
        Trains and evaluates a Kneighbors classifier.

        Args:
            features_test (sparse matrix): The feature matrix for the test data.
            features_train (sparse matrix): The feature matrix for the train data.
            features_unlabeled (sparse matrix): The feature matrix for the unlabeled data.
            preds_unlabeled (array): The predicted labels for the unlabeled data.
            run_object (Run): The run object.
            text_list_test_class (list): The actual labels for the test data.
            text_list_train_class (list): The actual labels for the train data.

        Returns:
            float: The score (accuracy) of the test dataset.
            float: The score (accuracy) of the train dataset.
            classifier: The classifier model
            number: The predictions of the classifier on the train dataset
        """
        clf = KNeighborsClassifier(n_neighbors=5)
        clf.fit(features_unlabeled, preds_unlabeled)
        score_train = clf.score(features_train, text_list_train_class)
        predictions_train = clf.predict(features_train)
        score_test = clf.score(features_test, text_list_test_class)
        classifier = Classifier.objects.get_or_create(
            type="KN", test_score=score_test, train_score=score_train
        )
        run_object.classifier = classifier[0]
        run_object.save()
        return score_test, score_train, clf, predictions_train

    def __classifier_logistic_regression(
        self,
        features_test,
        features_train,
        features_unlabeled,
        preds_unlabeled,
        run_object,
        text_list_test_class,
        text_list_train_class,
    ):
        """
        Trains and evaluates a logistic regression classifier.

        Args:
            features_test (sparse matrix): The feature matrix for the test data.
            features_train (sparse matrix): The feature matrix for the train data.
            features_unlabeled (sparse matrix): The feature matrix for the unlabeled data.
            preds_unlabeled (array): The predicted labels for the unlabeled data.
            run_object (Run): The run object.
            text_list_test_class (list): The actual labels for the test data.
            text_list_train_class (list): The actual labels for the train data.

        Returns:
            float: The score (accuracy) of the test dataset.
            float: The score (accuracy) of the train dataset.
            classifier: The classifier model
            number: The predictions of the classifier on the train dataset
        """
        clf = LogisticRegression()
        clf.fit(features_unlabeled, preds_unlabeled)
        score_train = clf.score(features_train, text_list_train_class)
        predictions_train = clf.predict(features_train)
        score_test = clf.score(features_test, text_list_test_class)
        classifier = Classifier.objects.get_or_create(
            type="LR", test_score=score_test, train_score=score_train
        )
        run_object.classifier = classifier[0]
        run_object.save()
        return score_test, score_train, clf, predictions_train

    def __call_feature_generation(
        self,
        range_x,
        range_y,
        run_object,
        selectedModelFeaturize,
        text_list_test,
        text_list_train,
        text_list_unlabeled,
    ):
        """
        Calls the feature generation service to extract features from the text data.

        Args:
           range_x (int): The lower boundary of the range for n-grams.
           range_y (int): The upper boundary of the range for n-grams.
           run_object (Run): The run object.
           selectedModelFeaturize (str): The feature extraction model to be applied.
           text_list_test (list): The list of test texts.
           text_list_train (list): The list of train texts.
           text_list_unlabeled (list): The list of unlabeled texts.

        Returns:
           - features_test: Features for the test texts.
           - features_train: Features for the train texts.
           - features_unlabeled: Features for the unlabeled texts.
        """
        featuregenerationservice = FeatureGenerationService()
        features_test, features_train, features_unlabeled = (
            featuregenerationservice.extraxt_features(
                range_x,
                range_y,
                selectedModelFeaturize,
                text_list_test,
                text_list_train,
                text_list_unlabeled,
                run_object,
            )
        )
        return features_test, features_train, features_unlabeled

    def __call_label_modell(
        self,
        base_learning_rate,
        l2,
        log_freq,
        n_epochs,
        numbers_of_labels,
        run_object,
        seed,
        selectedModelLabel,
        selectedTie,
    ):
        """
        Calls the labelmodel service to generate single labels for the unlabeled data.

        Args:
            base_learning_rate (float): The base learning rate for the label model.
            l2 (float): The L2 regularization parameter.
            log_freq (int): The log frequency..
            n_epochs (int): The number of epochs for training the label model.
            numbers_of_labels (int): The number of labels.
            run_object (Run): The run object.
            seed (int): The random seed.
            selectedModelLabel (str): The label model to be used.
            selectedTie (bool): The option how to handle tie cases in the label model.

        Returns:
            ndarray: The predicted labels for the unlabeled data.
        """
        labelmodelservice = LabelModelService()
        preds_unlabeled = labelmodelservice.label_model(
            run_object,
            selectedModelLabel,
            selectedTie,
            n_epochs,
            log_freq,
            seed,
            base_learning_rate,
            l2,
            numbers_of_labels,
        )
        run_object.preds_unlabeled = json.dumps(preds_unlabeled.tolist())
        run_object.save()
        return preds_unlabeled

    def __filter_abstain_in_dataset(
        self, text_list_unlabeled, preds_unlabeled, filterAbstain
    ):
        """
        Filters the datapoint with assigned Abstains out of the unlabeled dataset.

        Args:
            text_list_unlabeled (list): list of the texts of the unlabeled dataset
            preds_unlabeled (list): list of assigned labels of the unlabeled dataset.
            filterAbstain (bool): If true Abstain will be filtered, otherwise do nothing

        Returns:
            - list: list of texts
            - list: list of assigned labels.
        """
        if filterAbstain:
            filter_preds = []
            filter_text = []
            for i in range(0, len(text_list_unlabeled)):
                if preds_unlabeled[i] != -1:
                    filter_preds.append(preds_unlabeled[i])
                    filter_text.append(text_list_unlabeled[i])
            return filter_text, filter_preds
        return text_list_unlabeled, preds_unlabeled
