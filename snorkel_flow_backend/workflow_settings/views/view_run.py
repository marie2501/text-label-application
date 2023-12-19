import json
import sys
from io import StringIO

import numpy as np
from snorkel.labeling import labeling_function, PandasLFApplier, LFAnalysis
import pandas as pd


from rest_framework import status, authentication, viewsets
from rest_framework.parsers import JSONParser, FileUploadParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import HttpResponseForbidden, HttpResponseNotFound, HttpResponseBadRequest

from snorkel_flow_backend.settings import MEDIA_ROOT
from workflow_settings.models import Labelfunction, Run, File
from workflow_settings.serializers.serializers_run import RunCreateSerializer, RunSerializer


class RunView(viewsets.ViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated]
    parser_class = [JSONParser, FileUploadParser]


    # todo execude function - richtig machen später -> es fehlt noch das das datenset nach einem bestimmten ratio gespalten wird
    # Hier achten mit splitting id, da dieses labeld in test und train schon unterteil
    # später nochmal gucken
    def exec_run(self, request, *args, **kwargs):
        run_id = kwargs['pk']
        run = Run.objects.filter(pk=run_id)
        if run.exists():
            run_obeject = run[0]
            run_labelfunctions = run_obeject.labelfunctions.all()
            file = File.objects.filter(workflow_id=run[0].workflow_id)
            if file.exists():
                Labelfunction.objects.filter()
                file_name = file[0].__str__()
                file_path = "{root}/{name}".format(root=MEDIA_ROOT, name=file_name)
                imports = Labelfunction.objects.filter(workflow_id=run[0].workflow_id, type='import')
                if imports.exists():
                    try:
                        exec(imports[0].code, locals())

                        dataframe = pd.read_csv(file_path)
                        # hier nur unlabeled data
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

                        applier = PandasLFApplier(lfs=labelfunction_reference)
                        L_train_unlabeled = applier.apply(df=dataframe_unlabeled)
                        L_train_train = applier.apply(df=dataframe_train)

                        summary = LFAnalysis(L=L_train_unlabeled, lfs=labelfunction_reference).lf_summary()
                        summary_train = LFAnalysis(L=L_train_train, lfs=labelfunction_reference).lf_summary(Y=text_list_train_gold_labels)
                        labelmatrix = json.dumps(L_train_unlabeled.tolist())
                        run_obeject.labelfunction_summary = summary.to_json(orient='split')
                        run_obeject.labelmatrix = labelmatrix
                        run_obeject.labelfunction_summary_train = summary_train.to_json(orient='split')
                        run_obeject.save()
                        return Response(summary, status=status.HTTP_200_OK)
                    except:
                        error = str(sys.exc_info())
                        return Response(error, status=status.HTTP_400_BAD_REQUEST)
                else:
                    try:
                        dataframe = pd.read_csv(file_path)
                        # hier nur unlabeled data
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

                        applier = PandasLFApplier(lfs=labelfunction_reference)
                        L_train_unlabeled = applier.apply(df=dataframe_unlabeled)
                        L_train_train = applier.apply(df=dataframe_train)

                        summary = LFAnalysis(L=L_train_unlabeled, lfs=labelfunction_reference).lf_summary()
                        summary_train = LFAnalysis(L=L_train_train, lfs=labelfunction_reference).lf_summary(
                            Y=text_list_train_gold_labels)
                        labelmatrix = json.dumps(L_train_unlabeled.tolist())
                        run_obeject.labelfunction_summary = summary.to_json(orient='split')
                        run_obeject.labelmatrix = labelmatrix
                        run_obeject.labelfunction_summary_train = summary_train.to_json(orient='split')
                        run_obeject.save()
                        return Response(summary, status=status.HTTP_200_OK)
                    except:
                        error = str(sys.exc_info())
                        return Response(error, status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def get_analysis(self, request, *args, **kwargs):
        run_id = kwargs['pk']
        run = Run.objects.filter(pk=run_id)
        if run.exists():
            run_obeject_summary = run[0].labelfunction_summary
            run_obeject_summary_train = run[0].labelfunction_summary_train
            summary = pd.read_json(StringIO(run_obeject_summary), orient='split')
            summary_train = pd.read_json(StringIO(run_obeject_summary_train), orient='split')
            summary['index'] = summary.index
            summary_train = summary_train.rename(columns={"Emp. Acc.": "EmpAcc"})
            summary_train['index'] = summary_train.index
            print(summary_train)
            return Response({'summary': summary, 'summary_train': summary_train}, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)



    def get_run(self, request, *args, **kwargs):
        run_id = kwargs['pk']
        run = Run.objects.filter(pk=run_id)
        if run.exists():
            run_obj = run[0]
            run_serializer = RunSerializer(run_obj)
            return Response(run_serializer.data, status=status.HTTP_200_OK)
        return HttpResponseNotFound()


    def list_run(self, request, *args, **kwargs):
        workflow_id = kwargs['pk']
        labelfunction_run = Run.objects.filter(workflow_id=workflow_id)
        print(labelfunction_run)
        if labelfunction_run.exists():
            run_serializer = RunSerializer(labelfunction_run, many=True)
            return Response(run_serializer.data,status=status.HTTP_200_OK)
        return HttpResponseNotFound()

    def create_run(self, request, *args, **kwargs):
        workflow_id = kwargs['pk']
        run_serializer = RunCreateSerializer(data=request.data)
        if run_serializer.is_valid():
            run = run_serializer.save(creator=request.user, workflow_id=workflow_id)
            return Response(status=status.HTTP_201_CREATED)
        return Response(run_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


