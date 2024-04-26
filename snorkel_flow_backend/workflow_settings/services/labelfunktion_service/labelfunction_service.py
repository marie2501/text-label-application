import sys

from snorkel.labeling import PandasLFApplier, LFAnalysis
import pandas as pd

from zen_queries import fetch, queries_disabled

from rest_framework import status

from snorkel_flow_backend.settings import MEDIA_ROOT
from workflow_settings.models import Labelfunction, File, Run
from workflow_settings.serializers.serializers_labelfunction import LabelfunctionSerializer, LabelfunctionCreateSerializer

class LabelfunctionService:
    def get_imports(self, workflow_id):
        labelfunction = Labelfunction.objects.filter(workflow_id=workflow_id, type='import')
        if labelfunction.exists():
            serialziers_label = LabelfunctionSerializer(labelfunction[0])
            return status.HTTP_200_OK, serialziers_label.data
        return status.HTTP_404_NOT_FOUND, {"message": "Imports don't exists"}

    def compile_labelfunction(self, workflow_id, code):

        imports = Labelfunction.objects.filter(workflow_id=workflow_id, type='import')

        if imports.exists():
            import_code = imports[0].code
            try:
                exec(import_code, locals())
                exec(code, locals())
                return status.HTTP_200_OK, {"message": "The labelfunction compiled"}
            except:
                data = str(sys.exc_info())
                return status.HTTP_400_BAD_REQUEST, data
        return status.HTTP_404_NOT_FOUND, {"message": "No import statements where found. from snorkel.labeling import labeling_function needs to be imported"}

    # Imports und Code werden unter locals ausgeführt
    # todo python code sandboxing
    def test_labelfunction(self, workflow_id, code, name):

        file = File.objects.filter(workflow_id=workflow_id)

        if file.exists():
            file_name = file[0].__str__()
            file_path = "{root}/{name}".format(root=MEDIA_ROOT, name=file_name)

            imports = Labelfunction.objects.filter(workflow_id=workflow_id, type='import')
            if imports.exists():
                try:
                    import_code = imports[0].code

                    exec(import_code, locals())
                    exec(code, locals())
                    dataframe = pd.read_csv(file_path)
                    dataframe = dataframe.loc[(dataframe['splitting_id'] == 'unlabeled')]
                    local_var = locals()

                    lfs = [local_var[name]]
                    with queries_disabled():
                        applier = PandasLFApplier(lfs=lfs)
                        L_train = applier.apply(df=dataframe)
# todo hier wurde coverage durch summary getauscht im frontend anpassen
                    labelsummary = LFAnalysis(L=L_train, lfs=lfs).lf_summary()
                    return status.HTTP_200_OK, labelsummary
                except:
                    data = str(sys.exc_info())
                    return status.HTTP_400_BAD_REQUEST, data
            return status.HTTP_404_NOT_FOUND, {"message": "No import statements where found. from snorkel.labeling import labeling_function needs to be imported"}
        return status.HTTP_404_NOT_FOUND, {"message": "No data set has been uploaded"}

    def get_all_labelfunction_by_workflow_id(self, workflow_id):
        labelfunction = Labelfunction.objects.filter(workflow_id=workflow_id).exclude(type='import').order_by('creator')
        serialziers_label = LabelfunctionSerializer(labelfunction, many=True)
        return status.HTTP_200_OK, serialziers_label.data

    def get_labelfunction_by_id(self, labelfunction_id):
        labelfunction = Labelfunction.objects.filter(pk=labelfunction_id)
        if labelfunction.exists():
            serialziers_label = LabelfunctionSerializer(labelfunction[0])
            return status.HTTP_200_OK, serialziers_label.data
        return status.HTTP_404_NOT_FOUND, {"message": "The labelfunction does not exist"}

    def add_labelfunction(self, request_user, serialziers_label):
        if serialziers_label.is_valid():
            serialziers_label.save(creator=request_user)
            return status.HTTP_201_CREATED, {"message": "Labelfunction was successfully created"}
        return status.HTTP_400_BAD_REQUEST, serialziers_label.errors


# todo über permission klass nur labelfunktion creator, deletet und update

    def delete_labelfunction(self, labelfunction_id):
        labelfunction = Labelfunction.objects.filter(pk=labelfunction_id)
        if labelfunction.exists():
            labelfunktion_object = labelfunction[0]
            if not Run.objects.filter(workflow_id=labelfunktion_object.workflow_id).filter(labelfunctions__in=[labelfunktion_object]).exists():
                labelfunktion_object.delete()
                return status.HTTP_200_OK, {"message": "The labelfunction was successfully created"}
            return status.HTTP_400_BAD_REQUEST, {"message": "The label function cannot be deleted as long as it is used in a run"}
        return status.HTTP_404_NOT_FOUND, {"message": "The labelfunction does not exist"}

    def update_labelfunction(self, labelfunction_id, request_data):
        labelfunction = Labelfunction.objects.filter(pk=labelfunction_id)
        if labelfunction.exists():
            labelfunktion_object = labelfunction[0]
            serialziers_label = LabelfunctionCreateSerializer(labelfunktion_object, data=request_data, partial=True)
            if serialziers_label.is_valid():
                serialziers_label.save()
                return status.HTTP_200_OK, {"message": "The labelfunction was successfully updated"}
            return status.HTTP_400_BAD_REQUEST, serialziers_label.errors
        return status.HTTP_404_NOT_FOUND, {"message": "The labelfunction does not exist"}

    def update_import(self, workflow_id, request_data):
        labelfunction_filter = Labelfunction.objects.filter(workflow_id=workflow_id, type='import')
        if labelfunction_filter.exists():
            import_object = labelfunction_filter[0]
            serialziers_import = LabelfunctionCreateSerializer(import_object, data=request_data, partial=True)
            if serialziers_import.is_valid():
                serialziers_import.save()
                return status.HTTP_200_OK, {"message": "The imports were successfully updated"}
            return status.HTTP_400_BAD_REQUEST, serialziers_import.errors
        serialziers_import = LabelfunctionCreateSerializer(data=request_data)
        if serialziers_import.is_valid():
            serialziers_import.save()
            return status.HTTP_200_OK, {"message": "The imports were successfully updated"}
        return status.HTTP_400_BAD_REQUEST, serialziers_import.errors


