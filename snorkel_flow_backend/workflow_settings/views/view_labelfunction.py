import sys

from snorkel.labeling import PandasLFApplier, LFAnalysis
import pandas as pd

from zen_queries import fetch, queries_disabled

from rest_framework import status, authentication, viewsets
from rest_framework.parsers import JSONParser, FileUploadParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from snorkel_flow_backend.settings import MEDIA_ROOT
from workflow_settings.models import Labelfunction, File
from workflow_settings.serializers.serializers_labelfunction import LabelfunctionSerializer, LabelfunctionCreateSerializer


class LabelfunctionView(viewsets.ViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated]
    parser_class = [JSONParser, FileUploadParser]

    def get_imports(self, request, *args, **kwargs):
        workflow_id = kwargs['pk']
        labelfunction = Labelfunction.objects.filter(workflow_id=workflow_id, type='import')
        if labelfunction.exists():
            serialziers_label = LabelfunctionSerializer(labelfunction[0])
            return Response(serialziers_label.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def compile_labelfunction(self, request, *args, **kwargs):
        code = request.data['pythoncode']
        workflow_id = kwargs['pk']

        imports = Labelfunction.objects.filter(workflow_id=workflow_id, type='import')
        try:
            if imports.exists():
                import_code = imports[0].code
                exec(import_code, locals())
                exec(code, locals())
                data = 'Compiled'
                return Response(data, status=status.HTTP_200_OK)
            else:
                exec(code, locals())
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

        file = File.objects.filter(workflow_id=workflow_id)
        if file.exists():
            file_name = file[0].__str__()
            file_path = "{root}/{name}".format(root=MEDIA_ROOT, name=file_name)

            # get import Statements
            imports = Labelfunction.objects.filter(workflow_id=workflow_id, type='import')
            if imports.exists():
                try:
                    import_code = imports[0].code

                    exec(import_code, locals())
                    exec(code, locals())
                    # todo übers ganze datenset laufen lassen - unlabeld laufen lassen
                    dataframe = pd.read_csv(file_path)
                    dataframe = dataframe.loc[(dataframe['splitting_id'] == 'unlabeled')]
                    local_var = locals()

                    lfs = [local_var[name]]
                    with queries_disabled():
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

                    dataframe = pd.read_csv(file_path)
                    dataframe = dataframe.loc[(dataframe['splitting_id'] == 'unlabeled')]
                    local_var = locals()

                    lfs = [local_var[name]]

                    with queries_disabled():
                        applier = PandasLFApplier(lfs=lfs)
                        L_train = applier.apply(df=dataframe)

                    coverage = LFAnalysis(L=L_train, lfs=lfs).lf_coverages()[0]
                    return Response(coverage, status=status.HTTP_200_OK)
                except:
                    error = str(sys.exc_info())
                    return Response(error, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def get_all_labelfunction_by_workflow_id(self, request, *args, **kwargs):
        workflow_id = kwargs['pk']
        labelfunction = Labelfunction.objects.filter(workflow_id=workflow_id).exclude(type='import').order_by('creator')
        serialziers_label = LabelfunctionSerializer(labelfunction, many=True)
        return Response(serialziers_label.data, status=status.HTTP_200_OK)

    def get_labelfunction_by_id(self, request, *args, **kwargs):
        labelfunction = kwargs['pk']
        labelfunction = Labelfunction.objects.filter(pk= labelfunction)
        if labelfunction.exists():
            serialziers_label = LabelfunctionSerializer(labelfunction[0])
            return Response(serialziers_label.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)


    def add_labelfunction(self, request, *args, **kwargs):
        workflow_id = kwargs['pk']
        request_data = request.data
        request_data['workflow'] = workflow_id
        serialziers_label = LabelfunctionCreateSerializer(data=request_data)
        if serialziers_label.is_valid():
            serialziers_label.save(creator=request.user)
            return Response(status=status.HTTP_201_CREATED)
        return Response(serialziers_label.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete_labelfunction(self, request, *args, **kwargs):
        labelfunction_id = kwargs['pk']
        labelfunction = Labelfunction.objects.filter(pk=labelfunction_id)
        if labelfunction.exists():
            l = labelfunction[0]
            if l.creator == request.user:
                l.delete()
                return Response(status=status.HTTP_200_OK)
            return Response(status=status.HTTP_403_FORBIDDEN)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def update_labelfunction(self, request, *args, **kwargs):
        labelfunction_id = kwargs['pk']
        labelfunction = Labelfunction.objects.filter(pk=labelfunction_id)
        if labelfunction.exists():
            l = labelfunction[0]
            if (l.creator == request.user) or (l.type == 'import'):
                serialziers_label = LabelfunctionCreateSerializer(l, data=request.data, partial=True)
                if serialziers_label.is_valid():
                    serialziers_label.save()
                    return Response(status=status.HTTP_200_OK)
                return Response(serialziers_label.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_403_FORBIDDEN)
        return Response(status=status.HTTP_404_NOT_FOUND)


