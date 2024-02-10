from rest_framework import serializers

from workflow_settings.models import File
import pandas as pd

# serializer for the upload o datasets
class FileUploadSerializer(serializers.ModelSerializer):

    # validate if the correct colum names are present
    def validate(self, attrs):
        accepted_colum_names = ['corpus_id', 'entity_id', 'text', 'splitting_id', 'CLASS']

        file = attrs['file']
        file_header = pd.read_csv(file, nrows=0)

        header_list = file_header.columns.tolist()


        if not all(el in header_list for el in accepted_colum_names):
            raise serializers.ValidationError("The dataset must have the headers corpus_id, entity_id, text, splitting_id and CLASS")
        return attrs


    class Meta:
        model = File
        fields = ['file']

class FileUpdateSerializer(serializers.ModelSerializer):

    # validate if the correct colum names are present
    def validate(self, attrs):
        accepted_colum_names = ['corpus_id', 'entity_id', 'text', 'splitting_id', 'CLASS']

        file = attrs['file']
        file_header = pd.read_csv(file, nrows=0)

        header_list = file_header.columns.tolist()


        if not all(el in header_list for el in accepted_colum_names):
            raise serializers.ValidationError("The dataset must have the headers corpus_id, entity_id, text, splitting_id and CLASS")
        return attrs


    class Meta:
        model = File
        fields = ['file', 'id']


