import json

import pandas as pd
from django.http import HttpResponse
from rest_framework import status

from snorkel_flow_backend.settings import MEDIA_ROOT
from workflow_settings.models import File, Run


class FileDownloadService:

    def download_annotated_dataset(self, run_id):

        response = HttpResponse(content_type='text/csv', status=status.HTTP_200_OK)
        response['Content-Disposition'] = 'attachment; filename=filename.csv'

        run_filter = Run.objects.filter(pk=run_id)
        if run_filter.exists():
            run_object = run_filter[0]
            workflow_id = run_object.workflow.id
            file_filter = File.objects.filter(workflow_id=workflow_id)
            if file_filter.exists():
                file_object = file_filter[0]
                unlabeled_pred = list(json.loads(run_object.preds_unlabeled))
                file_name = file_object.__str__()
                file_path = "{root}/{name}".format(root=MEDIA_ROOT, name=file_name)
                dataframe = pd.read_csv(file_path)

                def get_new_value(row):
                    if row['splitting_id'] == 'unlabeled':
                        return unlabeled_pred.pop(0)
                    else:
                        return row['CLASS']


                dataframe['CLASS'] = dataframe.apply(get_new_value, axis=1)
                dataframe.to_csv(path_or_buf=response)

                return response, None, None
            return None, status.HTTP_404_NOT_FOUND, {"message": "There was no dataset uploaded"}
        return None, status.HTTP_404_NOT_FOUND, {"message": "The run doesn't exists"}
