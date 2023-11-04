from django.contrib.auth.models import User
from django.core.exceptions import NON_FIELD_ERRORS
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from workflow_settings.models import Workflow, Labelfunction, Run


class LabelfunctionSerializer(serializers.ModelSerializer):
    creator = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Labelfunction
        fields = ['id','creator','name', 'type', 'code']

class LabelfunctionCreateSerializer(serializers.ModelSerializer):
    workflow = serializers.PrimaryKeyRelatedField(many=False, read_only=False, queryset=Workflow.objects.all())

    class Meta:
        model = Labelfunction
        fields = ['name', 'type', 'code', 'workflow']

        validators = [
            UniqueTogetherValidator(
                queryset=Labelfunction.objects.all(),
                fields=['workflow', 'name'],
                message="A Labelfunction with this name already exists."
            )
        ]
