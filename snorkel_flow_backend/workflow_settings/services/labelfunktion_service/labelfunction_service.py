import sys

import numpy as np
from snorkel.labeling import PandasLFApplier, LFAnalysis
import pandas as pd

from zen_queries import fetch, queries_disabled

from rest_framework import status

from snorkel_flow_backend.settings import MEDIA_ROOT
from workflow_settings.models import Labelfunction, File, Run, Workflow
from workflow_settings.serializers.serializers_labelfunction import LabelfunctionSerializer, LabelfunctionCreateSerializer

class LabelfunctionService:
    def get_import_labels(self, workflow_id, type):
        labelfunction = Labelfunction.objects.filter(workflow_id=workflow_id, type=type)
        if labelfunction.exists():
            serialziers_label = LabelfunctionSerializer(labelfunction[0])
            return status.HTTP_200_OK, serialziers_label.data
        return status.HTTP_404_NOT_FOUND, {"message": f"{type} don't exists"}

    def get_labels(self, workflow_id):
        labelfunction = Labelfunction.objects.filter(workflow_id=workflow_id, type='labels')
        if labelfunction.exists():
            serialziers_label = LabelfunctionSerializer(labelfunction[0])
            return status.HTTP_200_OK, serialziers_label.data
        return status.HTTP_404_NOT_FOUND, {"message": "Labels don't exists"}

    def __checkLabels(self, workflow_id, L_train_list, L_unlabeled_list):
        labelfunction_filter = Labelfunction.objects.filter(workflow_id=workflow_id, type='labels')
        if labelfunction_filter.exists():
            labelfunction_object_code = labelfunction_filter[0].code
            labels_split = labelfunction_object_code.split()
            labels_split.remove('=')
            while '=' in labels_split:
                labels_split.remove('=')
            L_train_list.extend(L_unlabeled_list)

            for el in L_train_list:
                if str(el) not in labels_split:
                    raise ValueError(f'The label { el } was not spezified by the workflow creator')


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
                labels = Labelfunction.objects.filter(workflow_id=workflow_id, type='labels')
                if labels.exists():
                    labels_code = labels[0].code
                    return self.__test_on_dataset(code, file_path, imports, name, workflow_id, labels_code)
                return self.__test_on_dataset(code, file_path, imports, name, workflow_id)
            return status.HTTP_404_NOT_FOUND, {"message": "No import statements where found. from snorkel.labeling import labeling_function needs to be imported"}
        return status.HTTP_404_NOT_FOUND, {"message": "No data set has been uploaded"}

    def __test_on_dataset(self, code, file_path, imports, name, workflow_id, labels_code=''):
        try:
            import_code = imports[0].code
            exec(import_code, locals())
            exec(labels_code, locals())
            exec(code, locals())
            dataframe = pd.read_csv(file_path)
            dataframe_unlabeled = dataframe.loc[(dataframe['splitting_id'] == 'unlabeled')]
            dataframe_train = dataframe.loc[(dataframe['splitting_id'] == 'train')]
            text_list_train_gold_labels = np.array(dataframe_train['CLASS'].tolist())
            local_var = locals()
            lfs = [local_var[name]]
            with queries_disabled():
                applier = PandasLFApplier(lfs=lfs)
                L_unlabeled = applier.apply(df=dataframe_unlabeled)
                L_train = applier.apply(df=dataframe_train)
            L_train_list = np.array(L_train).flatten().tolist()
            L_unlabeled_list = np.array(L_unlabeled).flatten().tolist()
            self.__checkLabels(workflow_id, L_train_list, L_unlabeled_list)
            labelsummary_unlabeled = LFAnalysis(L=L_unlabeled, lfs=lfs).lf_summary()
            labelsummary_train = LFAnalysis(L=L_train, lfs=lfs).lf_summary(Y=text_list_train_gold_labels)
            labelsummary_unlabeled['index'] = labelsummary_unlabeled.index
            labelsummary_train = labelsummary_train.rename(columns={"Emp. Acc.": "EmpAcc"})
            labelsummary_train['index'] = labelsummary_train.index
            return status.HTTP_200_OK, {'summary': labelsummary_unlabeled, 'summary_train': labelsummary_train}
        except:
            data = str(sys.exc_info())
            return status.HTTP_400_BAD_REQUEST, data

    def get_all_labelfunction_by_workflow_id(self, workflow_id):
        labelfunction = Labelfunction.objects.filter(workflow_id=workflow_id).exclude(type='import').exclude(type='labels').order_by('creator')
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
            labelfunction = serialziers_label.save(creator=request_user)
            return status.HTTP_201_CREATED, {'lid': labelfunction.id}
        return status.HTTP_400_BAD_REQUEST, serialziers_label.errors


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
                labelfunction_updated = serialziers_label.save()
                return status.HTTP_200_OK, {'lid': labelfunction_updated.id}
            return status.HTTP_400_BAD_REQUEST, serialziers_label.errors
        return status.HTTP_404_NOT_FOUND, {"message": "The labelfunction does not exist"}

    def update_import_labels(self, workflow_id, request_data, type):
        labelfunction_filter = Labelfunction.objects.filter(workflow_id=workflow_id, type=type)
        if labelfunction_filter.exists():
            import_object = labelfunction_filter[0]
            try:
                import_code = request_data['code']
                exec(import_code, locals())
                serialziers_import = LabelfunctionCreateSerializer(import_object, data=request_data, partial=True)
                if serialziers_import.is_valid():
                    serialziers_import.save()
                    return status.HTTP_200_OK, {"message": f"The {type} were successfully updated"}
                return status.HTTP_400_BAD_REQUEST, serialziers_import.errors
            except:
                data = str(sys.exc_info())
                return status.HTTP_400_BAD_REQUEST, data
        try:
            import_code = request_data['code']
            exec(import_code, locals())
            serialziers_import = LabelfunctionCreateSerializer(data=request_data)
            if serialziers_import.is_valid():
                serialziers_import.save()
                return status.HTTP_200_OK, {"message": f"The {type} were successfully created"}
            return status.HTTP_400_BAD_REQUEST, serialziers_import.errors
        except:
            data = str(sys.exc_info())
            return status.HTTP_400_BAD_REQUEST, data


