from rest_framework import serializers
from snorkel.labeling.model import LabelModel

from workflow_settings.models import Run, Feature, Classifier
from workflow_settings.serializers.serializers_labelfunction import LabelfunctionSerializer


class RunCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Run
        fields = ['labelfunctions']


class RunSerializer(serializers.ModelSerializer):
    creator = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    labelfunctions = LabelfunctionSerializer(many=True, read_only=True)
    class Meta:
        model = Run
        fields = ['id', 'creator', 'labelfunctions', 'creation_date']

class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = ['type', 'range_x', 'range_y']

class LabelModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabelModel
        fields = ['type']

class ClassifierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classifier
        fields = ['type', 'test_score', 'train_score']