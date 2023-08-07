from rest_framework import serializers

from workflow_settings.models import File
from workflow_settings.models import Workflow


class FileUploadSerializer(serializers.ModelSerializer):

    class Meta:
        model = File
        fields = ['file']


