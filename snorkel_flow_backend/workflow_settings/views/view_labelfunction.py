import json
import sys

from snorkel.labeling import labeling_function, PandasLFApplier, LFAnalysis
import pandas as pd


from rest_framework import status, authentication, viewsets
from rest_framework.parsers import JSONParser, FileUploadParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import HttpResponseForbidden, HttpResponseNotFound, HttpResponseBadRequest

from snorkel_flow_backend.settings import MEDIA_ROOT
from workflow_settings.models import Labelfunction
from workflow_settings.serializers.serializers_labelfunction import LabelfunctionSerializer, LabelfunctionCreateSerializer


class LabelfunctionView(viewsets.ViewSet):
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

    # Datenbank

    def get_imports(self, request, *args, **kwargs):
        workflow_id = kwargs['pk']
        labelfunction = Labelfunction.objects.filter(workflow_id=workflow_id, type='import')
        if labelfunction.exists():
            serialziers_label = LabelfunctionSerializer(labelfunction[0])
            return Response(serialziers_label.data, status=status.HTTP_200_OK)

    def compile_labelfunction(self, request, *args, **kwargs):
        code = request.data['pythoncode']
        try:
            exec(code)
            data = 'Compiled'
            return Response(data, status=status.HTTP_200_OK)
        except:
            error = str(sys.exc_info())
            return Response(error, status=status.HTTP_400_BAD_REQUEST)


    # Imports und Code werden unter locals ausgeführt
    def test_labelfunction(self, request, *args, **kwargs):
        workflow_id = kwargs['pk']
        code = request.data['pythoncode']
        name = request.data['name']
        print(request.data)
        # todo später ändern
        file_path = "{root}/{name}".format(root=MEDIA_ROOT, name='11/file/marie/test_data.csv')

        # get import Statements
        imports = Labelfunction.objects.filter(workflow_id=workflow_id, type='import')
        if imports.exists():
            try:
                exec(imports[0].code, locals())
                exec(code, locals())
                print(file_path)
                # todo übers ganze datenset laufen lassen
                dataframe = pd.read_csv(file_path, nrows=15)
                local_var = locals()

                lfs = [local_var[name]]
                applier = PandasLFApplier(lfs=lfs)

                L_train = applier.apply(df=dataframe)

                coverage = LFAnalysis(L=L_train, lfs=lfs).lf_coverages()[0]
                return Response(coverage, status=status.HTTP_200_OK)
            except:
                error = str(sys.exc_info())
                return Response(error, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                exec(code, locals())

                dataframe = pd.read_csv(file_path, nrows=15)
                local_var = locals()

                lfs = [local_var[name]]
                applier = PandasLFApplier(lfs=lfs)

                L_train = applier.apply(df=dataframe)

                coverage = LFAnalysis(L=L_train, lfs=lfs).lf_coverages()[0]
                return Response(coverage, status=status.HTTP_200_OK)
            except:
                error = str(sys.exc_info())
                return Response(error, status=status.HTTP_400_BAD_REQUEST)

    def get_all_labelfunction_by_workflow_id(self, request, *args, **kwargs):
        workflow_id = kwargs['pk']
        labelfunction = Labelfunction.objects.filter(workflow_id=workflow_id).order_by('creator')
        serialziers_label = LabelfunctionSerializer(labelfunction, many=True)
        return Response(serialziers_label.data, status=status.HTTP_200_OK)

    def add_labelfunction(self, request, *args, **kwargs):
        workflow_id = kwargs['pk']
        serialziers_label = LabelfunctionCreateSerializer(data=request.data)
        if serialziers_label.is_valid():
            serialziers_label.save(workflow_id=workflow_id, creator=request.user)
            return Response(status=status.HTTP_201_CREATED)
        return HttpResponseBadRequest()

    def delete_labelfunction(self, request, *args, **kwargs):
        labelfunction_id = kwargs['pk']
        labelfunction = Labelfunction.objects.filter(pk=labelfunction_id)
        if labelfunction.exists():
            l = labelfunction[0]
            if l.creator == request.user:
                l.delete()
                return Response(status=status.HTTP_200_OK)
            return HttpResponseForbidden()
        return HttpResponseNotFound()

    def update_labelfunction(self, request, *args, **kwargs):
        labelfunction_id = kwargs['pk']
        labelfunction = Labelfunction.objects.filter(pk=labelfunction_id)
        if labelfunction.exists():
            l = labelfunction[0]
            if l.creator == request.user:
                serialziers_label = LabelfunctionSerializer(l, data=request.data, partial=True)
                if serialziers_label.is_valid():
                    serialziers_label.save()
                    return Response(status=status.HTTP_200_OK)
                return HttpResponseBadRequest()
            return HttpResponseForbidden()
        return HttpResponseNotFound()

#         # todo funktion noch nicht getestet
#     def get_labelfunction_run(self, request, *args, **kwargs):
#         labelfunction_run_id = kwargs['pk']
#         labelfunction_run = Labelfunction_Run.objects.filter(pk=labelfunction_run_id)
#         if labelfunction_run.exists():
#             l = labelfunction_run[0]
#             with open(l.file.path, 'r') as file:
#                 yaml_content = yaml.safe_load(file)
#             print(yaml_content)
#             return Response(yaml_content, status=status.HTTP_200_OK)
#         return HttpResponseNotFound()
#
# # File
#     # Store the functions which are to be used in a run as a yml file
#     # todo funktion noch nicht getestet
#     def create_labelfunction_run(self, request, *args, **kwargs):
#         workflow_id = kwargs['pk']
#         file_serializer = FileUploadLabelfunctionSerializer(data=request.data)
#         if file_serializer.is_valid():
#             file = file_serializer.save(creator=request.user, workflow_id=workflow_id)
#             return Response(status=status.HTTP_201_CREATED)
#         return HttpResponseBadRequest()


