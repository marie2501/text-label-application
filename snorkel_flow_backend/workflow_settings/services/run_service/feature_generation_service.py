from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from rest_framework import status
from workflow_settings.models import Feature, Run
from workflow_settings.serializers.serializers_run import FeatureSerializer


class FeatureGenerationService:

    def get_feature_by_run_id(self, run_id):
        run_filter = Run.objects.filter(pk=run_id)
        if run_filter.exists():
            run_object = run_filter[0]
            feature_serializer = FeatureSerializer(data=run_object.feature)
            return status.HTTP_200_OK, feature_serializer.data
        return status.HTTP_404_NOT_FOUND, {"message": "Run object doesn't exists"}

    def extraxt_features(self, range_x, range_y, selectedModelFeaturize, text_list_test, text_list_train,
                         text_list_unlabeled, run_object):
        if selectedModelFeaturize == 'Bag of words':
            feature = Feature.objects.get_or_create(range_x=range_x, range_y=range_y, type='BW')
            run_object.feature = feature[0]
            run_object.save()
            return self.__bag_of_words(range_x, range_y, text_list_test, text_list_train, text_list_unlabeled)
        elif selectedModelFeaturize == 'TFIDF':
            feature = Feature.objects.get_or_create(range_x=range_x, range_y=range_y, type='TF')
            run_object.feature = feature[0]
            run_object.save()
            return self.__tfidf(range_x, range_y, text_list_test, text_list_train, text_list_unlabeled)

    def __tfidf(self,range_x, range_y, text_list_test, text_list_train, text_list_unlabeled):
        vectorizer = TfidfVectorizer(ngram_range=(range_x, range_y))
        vectorizer.fit(text_list_unlabeled)
        features_unlabeled = vectorizer.transform(text_list_unlabeled)
        features_train = vectorizer.transform(text_list_train)
        features_test = vectorizer.transform(text_list_test)
        return features_test, features_train, features_unlabeled

    def __bag_of_words(self, range_x, range_y, text_list_test, text_list_train, text_list_unlabeled):
        vectorizer = CountVectorizer(ngram_range=(range_x, range_y))
        vectorizer.fit(text_list_unlabeled)
        features_unlabeled = vectorizer.transform(text_list_unlabeled)
        features_train = vectorizer.transform(text_list_train)
        features_test = vectorizer.transform(text_list_test)
        return features_test, features_train, features_unlabeled


