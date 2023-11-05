from rest_framework import serializers
from workflow_settings.models import Run
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