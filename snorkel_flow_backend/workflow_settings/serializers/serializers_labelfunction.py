from django.contrib.auth.models import User
from django.core.exceptions import NON_FIELD_ERRORS
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from workflow_settings.models import Workflow, Labelfunction, Labelfunction_Run


class LabelfunctionSerializer(serializers.ModelSerializer):
    creator = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Labelfunction
        fields = ['id','creator','name', 'type', 'code']

class LabelfunctionCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Labelfunction
        fields = ['name', 'type', 'code']

class LabelfunctionRunSerializer(serializers.ModelSerializer):
    creator = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Labelfunction_Run
        fields = ['creator', 'file', 'creation_date']