import json
import sys
from io import StringIO

import numpy as np
from snorkel.labeling import PandasLFApplier, LFAnalysis
import pandas as pd
from zen_queries import fetch, queries_disabled


from rest_framework import status
from rest_framework.response import Response

from snorkel_flow_backend.settings import MEDIA_ROOT
from workflow_settings.models import Labelfunction, Run, File
from workflow_settings.serializers.serializers_run import RunCreateSerializer, RunSerializer


class RunService:

    def get_access(self, run_id, request_user):
        run_filter = Run.objects.filter(pk=run_id, creator=request_user)
        if run_filter.exists():
            return status.HTTP_200_OK, True
        return status.HTTP_200_OK, False

    def exec_run(self, run_id):
        run_filter = Run.objects.filter(pk=run_id)
        if run_filter.exists():
            run_obeject = run_filter[0]
            run_labelfunctions = run_obeject.labelfunctions.all()
            file = File.objects.filter(workflow_id=run_filter[0].workflow_id)
            if file.exists():
                file_name = file[0].__str__()
                file_path = "{root}/{name}".format(root=MEDIA_ROOT, name=file_name)
                imports = Labelfunction.objects.filter(workflow_id=run_filter[0].workflow_id, type='import')
                if imports.exists():
                    try:
                        exec(imports[0].code, locals())

                        dataframe = pd.read_csv(file_path)

                        dataframe_unlabeled = dataframe.loc[(dataframe['splitting_id'] == 'unlabeled')]
                        dataframe_train = dataframe.loc[(dataframe['splitting_id'] == 'train')]
                        text_list_train_gold_labels = np.array(dataframe_train['CLASS'].tolist())

                        labelfunction_names = []
                        for item in run_labelfunctions:
                            exec(item.code, locals())
                            labelfunction_names.append(item.name)
                        local_vars = locals()

                        labelfunction_reference = []
                        for label in labelfunction_names:
                            labelfunction_reference.append(local_vars[label])

                        with queries_disabled():
                            applier = PandasLFApplier(lfs=labelfunction_reference)
                            L_train_unlabeled = applier.apply(df=dataframe_unlabeled)
                            L_train_train = applier.apply(df=dataframe_train)

                        summary = LFAnalysis(L=L_train_unlabeled, lfs=labelfunction_reference).lf_summary()
                        summary_train = LFAnalysis(L=L_train_train, lfs=labelfunction_reference).lf_summary(Y=text_list_train_gold_labels)
                        summary['index'] = summary.index
                        summary_train = summary_train.rename(columns={"Emp. Acc.": "EmpAcc"})
                        summary_train['index'] = summary_train.index

                        data = {'summary': summary, 'summary_train': summary_train}
                        labelmatrix = json.dumps(L_train_unlabeled.tolist())
                        run_obeject.labelfunction_summary = summary.to_json(orient='split')
                        run_obeject.labelmatrix = labelmatrix
                        run_obeject.labelfunction_summary_train = summary_train.to_json(orient='split')
                        run_obeject.save()
                        return status.HTTP_200_OK, data
                    except:
                        data = str(sys.exc_info())
                        return status.HTTP_400_BAD_REQUEST, data
        return status.HTTP_404_NOT_FOUND, {"message": "The run does not exist"}

# todo get analysis wegmachen und direkt in exekute run machen
#     def get_analysis(self, run_id):
#         run = Run.objects.filter(pk=run_id)
#         if run.exists():
#             if run[0].labelfunction_summary is not None:
#                 run_obeject_summary = run[0].labelfunction_summary
#                 run_obeject_summary_train = run[0].labelfunction_summary_train
#                 summary = pd.read_json(StringIO(run_obeject_summary), orient='split')
#                 summary_train = pd.read_json(StringIO(run_obeject_summary_train), orient='split')
#                 summary['index'] = summary.index
#                 summary_train = summary_train.rename(columns={"Emp. Acc.": "Empirical Accuracy"})
#                 summary_train['index'] = summary_train.index
#                 return status.HTTP_200_OK, {'summary': summary, 'summary_train': summary_train}
#             error = 'The run has not yet been executed by the creator.'
#             return status.HTTP_400_BAD_REQUEST, error
#         return status.HTTP_404_NOT_FOUND, {"message": "The run object does not exist"}



    def get_run(self, run_id):
        run = Run.objects.filter(pk=run_id)
        if run.exists():
            run_obj = run[0]
            run_serializer = RunSerializer(run_obj)
            return status.HTTP_200_OK, run_serializer.data
        return status.HTTP_404_NOT_FOUND, {"message": "The run object does not exist"}


    def list_run(self, workflow_id, request_user):
        labelfunction_run = Run.objects.filter(workflow_id=workflow_id, creator=request_user)
        if labelfunction_run.exists():
            run_serializer = RunSerializer(labelfunction_run, many=True)
            return status.HTTP_200_OK, run_serializer.data
        return status.HTTP_200_OK, []

    def create_run(self, workflow_id, run_serializer, request_user):
        if run_serializer.is_valid():
            print(run_serializer)
            print('hhsdhashkdhkashdhaskhdkjhadshadhshdhakhdakjhdh/n')
            run_serializer.save(creator=request_user, workflow_id=workflow_id)
            return status.HTTP_201_CREATED, {"message": "Run was successfuly created"}
        return status.HTTP_400_BAD_REQUEST, run_serializer.errors

    def update_run(self, run_id, request_data):
        run_obj = Run.objects.filter(pk=run_id)
        if run_obj.exists():
            run = run_obj[0]
            run_serializer = RunCreateSerializer(run, data=request_data, partial=True)
            if run_serializer.is_valid():
                run_serializer.save()
                return status.HTTP_201_CREATED, {"message": "Run was successfuly created"}
            return status.HTTP_400_BAD_REQUEST, run_serializer.errors
        return status.HTTP_404_NOT_FOUND, {"message": "The run object does not exist"}
