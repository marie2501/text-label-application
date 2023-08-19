from rest_framework import serializers

from workflow_settings.models import File, Labelfunction, Labelfunction_Run
from workflow_settings.models import Workflow


class FileUploadSerializer(serializers.ModelSerializer):

    class Meta:
        model = File
        fields = ['file']

class FileUploadLabelfunctionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Labelfunction
        fields = ['file']


