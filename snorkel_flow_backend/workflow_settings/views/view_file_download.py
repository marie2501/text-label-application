import json

import numpy as np
import pandas as pd
from django.http import HttpResponse
from rest_framework import status, authentication
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from snorkel_flow_backend.settings import MEDIA_ROOT
from workflow_settings.serializers.serializers_file import FileUploadSerializer
from workflow_settings.models import File, Workflow, Run

class FileDownView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    parser_class = [FileUploadParser]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        run_id = kwargs['pk']

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=filename.csv'

        run_obj = Run.objects.filter(pk=run_id)
        if run_obj.exists():
            run_obj = run_obj[0]
            unlabeled_pred = list(json.loads(run_obj.preds_unlabeled))

            workflow_id = run_obj.workflow.id

            if File.objects.filter(workflow_id=workflow_id).exists():

                def get_new_value(row):
                    if row['splitting_id'] == 'unlabeled':
                        return unlabeled_pred.pop(0)
                    else:
                        return row['CLASS']

                file = File.objects.get(workflow_id=workflow_id)
                file_name = file.__str__()
                file_path = "{root}/{name}".format(root=MEDIA_ROOT, name=file_name)
                dataframe = pd.read_csv(file_path)
                dataframe['CLASS'] = dataframe.apply(get_new_value, axis=1)

                dataframe.to_csv(path_or_buf=response)
                return response
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_404_NOT_FOUND)

