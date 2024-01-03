from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from workflow_settings.models import Workflow

class UserAddRelSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id']

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']


class WorkflowCreateSerializer(serializers.ModelSerializer):
    creator = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Workflow
        fields = ['creator', 'is_public', 'title']

        validators = [
            UniqueTogetherValidator(
                queryset=Workflow.objects.all(),
                fields=['creator', 'title'],
                message="A workflow with this title already exists."
            )
        ]


class WorkflowSerializer(serializers.ModelSerializer):
    creator = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
     )
    
    class Meta:
        model = Workflow
        fields = '__all__'
