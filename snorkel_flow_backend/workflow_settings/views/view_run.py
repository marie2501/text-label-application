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
from workflow_settings.serializers.serializers_run import RunCreateSerializer


class RunView(viewsets.ViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated]
    parser_class = [JSONParser, FileUploadParser]


    # todo execude function - richtig machen später
    # def exec_labelfunction_run(self, request, *args, **kwargs):
    #     labelfunction_run_id = kwargs['pk']
    #     labelfunction_run = Labelfunction_Run.objects.filter(pk=labelfunction_run_id)
    #     if labelfunction_run.exists():
    #         l = labelfunction_run[0]
    #         file_path = "{root}/{name}".format(root=MEDIA_ROOT, name='data_test/Youtube05-Shakira.csv')
    #         dataframe = pd.read_csv(file_path)
    #         file_path_Y = "{root}/{name}".format(root=MEDIA_ROOT, name='data_test/test.yaml')
    #         with open(file_path_Y, 'r') as file:
    #             yaml_content = yaml.safe_load(file)
    #
    #         labelfunction_names = []
    #         for item in yaml_content:
    #             exec(item['code'])
    #             labelfunction_names.append(item['name'])
    #         myVars = locals()
    #         print(type(myVars[labelfunction_names[0]]))
    #         x = [myVars[labelfunction_names[0]], myVars[labelfunction_names[1]]]
    #         applier = PandasLFApplier(lfs=x)
    #         L_train = applier.apply(df=dataframe)
    #         print(L_train)
    #         return Response(yaml_content, status=status.HTTP_200_OK)
    #     return HttpResponseNotFound()


        # todo funktion noch nicht getestet
    def get_run(self, request, *args, **kwargs):
        labelfunction_run_id = kwargs['pk']
        labelfunction_run = Run.objects.filter(pk=labelfunction_run_id)
        if labelfunction_run.exists():
            l = labelfunction_run[0]
            # with open(l.file.path, 'r') as file:
            #     yaml_content = yaml.safe_load(file)
            # print(yaml_content)
            return Response(status=status.HTTP_200_OK)
        return HttpResponseNotFound()
#

    def create_run(self, request, *args, **kwargs):
        workflow_id = kwargs['pk']
        run_serializer = RunCreateSerializer(data=request.data)
        print(run_serializer)
        if run_serializer.is_valid():
            run = run_serializer.save(creator=request.user, workflow_id=workflow_id)
            return Response(status=status.HTTP_201_CREATED)
        return Response(run_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


