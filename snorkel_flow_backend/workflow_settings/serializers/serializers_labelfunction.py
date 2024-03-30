from django.contrib.auth.models import User
from django.core.exceptions import NON_FIELD_ERRORS
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from workflow_settings.models import Workflow, Labelfunction


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
    def validate(self, data):
        type = data.get('type')
        code = data.get('code')

        not_allowed_modules = ['os', 'shutil', 'subprocess', 'pickle', 'openpyxl',
                               'requests', 'paramiko', 'Crypto', 'BeautifulSoup', 'sys']

        if type == 'import':
            for modul in not_allowed_modules:
                if modul in code:
                    raise serializers.ValidationError(f"Code cannot contain {modul} for type 'import'.")
        else:
            if 'import' in code:
                raise serializers.ValidationError("Code cannot contain an import.")

        return data

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
