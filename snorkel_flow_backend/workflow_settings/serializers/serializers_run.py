from rest_framework import serializers
from workflow_settings.models import Run




class RunCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Run
        fields = ['splitting_ratio_labeled_test', 'labelfunctions']


class RunSerializer(serializers.ModelSerializer):
    creator = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Run
        fields = ['creator', 'splitting_ratio_labeled_test', 'labelfunctions', 'creation_date']