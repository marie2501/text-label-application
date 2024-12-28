import numpy as np
from rest_framework import serializers

from workflow_settings.models import File
import pandas as pd

# serializer for the upload o datasets
class FileUploadSerializer(serializers.ModelSerializer):

    # validate if the correct colum names are present
    def validate(self, attrs):
        accepted_colum_names = ['corpus_id', 'entity_id', 'text', 'splitting_id', 'class']

        file = attrs['file']
        dataframe = pd.read_csv(file)
        file_header = dataframe.head(0)

        header_list = file_header.columns.tolist()

        if not all(el in header_list for el in accepted_colum_names):
            raise serializers.ValidationError("The dataset must have the headers corpus_id, entity_id, text, splitting_id and class")

        if (-1 in dataframe['class'].values) or ('abstain' in np.char.lower(dataframe['class'].values.astype(str))):
            raise serializers.ValidationError(
                "-1 or abstain kann not be in the dataset")

        return attrs


    class Meta:
        model = File
        fields = ['file']



