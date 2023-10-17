import json
import sys

from snorkel.labeling import labeling_function, PandasLFApplier
import pandas as pd


from rest_framework import status, authentication, viewsets
from rest_framework.parsers import JSONParser, FileUploadParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import HttpResponseForbidden, HttpResponseNotFound, HttpResponseBadRequest

from snorkel_flow_backend.settings import MEDIA_ROOT
from workflow_settings.models import Labelfunction, Run
from workflow_settings.serializers.serializers_labelfunction import LabelfunctionSerializer, LabelfunctionCreateSerializer
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
            file_name = run_obeject.used_file.__str__()
            file_path = "{root}/{name}".format(root=MEDIA_ROOT, name=file_name)

            dataframe = pd.read_csv(file_path)
            # hier nur train
            dataframe = dataframe.loc[(dataframe['splitting_id'] == 'train') | (dataframe['splitting_id'] == 'test')]
            print(dataframe)
            labelfunction_names = []
            for item in run_labelfunctions:
                exec(item.code)
                labelfunction_names.append(item.name)
            local_vars = locals()
            labelfunction_reference = []
            for label in labelfunction_names:
                labelfunction_reference.append(local_vars[label])
            applier = PandasLFApplier(lfs=labelfunction_reference)
            L_train = applier.apply(df=dataframe)
            labelmatrix = json.dumps(L_train.tolist())

            run_obeject.labelmatrix = labelmatrix
            run_obeject.save()
            return Response(status=status.HTTP_200_OK)
        return HttpResponseNotFound()


    def get_run(self, request, *args, **kwargs):
        run_id = kwargs['pk']
        run = Run.objects.filter(pk=run_id)
        if run.exists():
            l = run[0]
            run_serializer = RunSerializer(l)
            return Response(run_serializer.data, status=status.HTTP_200_OK)
        return HttpResponseNotFound()


    def list_run(self, request, *args, **kwargs):
        workflow_id = kwargs['pk']
        labelfunction_run = Run.objects.filter(workflow_id=workflow_id)
        if labelfunction_run.exists():
            run_serializer = RunSerializer(labelfunction_run, many=True)
            return Response(run_serializer.data,status=status.HTTP_200_OK)
        return HttpResponseNotFound()

    def create_run(self, request, *args, **kwargs):
        workflow_id = kwargs['pk']
        run_serializer = RunCreateSerializer(data=request.data)
        print(run_serializer)
        if run_serializer.is_valid():
            run = run_serializer.save(creator=request.user, workflow_id=workflow_id)
            return Response(status=status.HTTP_201_CREATED)
        return Response(run_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


