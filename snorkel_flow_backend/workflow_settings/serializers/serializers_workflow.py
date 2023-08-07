from django.contrib.auth.models import User
from django.core.exceptions import NON_FIELD_ERRORS
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from workflow_settings.models import Workflow

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id']


class WorkflowCreateSerializer(serializers.ModelSerializer):
    creator = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Workflow
        fields = ['creator', 'is_public', 'title']

        validators = [
            UniqueTogetherValidator(
                queryset=Workflow.objects.all(),
                fields=['creator', 'title']
            )
        ]

        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "A workflow with this title already exists.",
            }
        }


class WorkflowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workflow
        fields = '__all__'
