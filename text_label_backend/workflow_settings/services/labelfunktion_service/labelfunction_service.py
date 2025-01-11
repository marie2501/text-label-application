"""
LabelfunctionService.py

The module provides a service that offers functionalities for
the creation and management of labelling functions.

Classes:
- LabelfunctionService
"""

import sys

import numpy as np
from snorkel.labeling import PandasLFApplier, LFAnalysis
import pandas as pd
from workflow_settings.services.validate_service.validate_functions_service import validate_code_for_imports_only, execute_code_in_safe_env, validate_labelfunction
from zen_queries import fetch, queries_disabled

from rest_framework import status

from text_label_backend.settings import MEDIA_ROOT
from workflow_settings.models import Labelfunction, File, Run
from workflow_settings.serializers.serializers_labelfunction import (
    LabelfunctionSerializer,
    LabelfunctionCreateSerializer,
)


class LabelfunctionService:
    """
    Service class for for the creation and management of labelling functions.

    Methods:
        - get_import_labels(workflow_id, type):
            Retrieves a labelfunction of the type import or labels
            for a specified workflow.

        - get_labels(workflow_id):
            Retrieves the labels for a specified workflow which were
            provided by the workflow creator.

        - compile_labelfunction(workflow_id, code):
            Compiles the labelfunction code with the imports of a specified workflow.

        - test_labelfunction(workflow_id, code, name):
            Tests the labelfunction code on the uploaded dataset.

        - get_all_labelfunction_by_workflow_id(workflow_id):
            Retrieves all labelfunctions for a specified workflow.

        - get_labelfunction_by_id(labelfunction_id):
            Retrieves a labelfunction by its ID.

        - add_labelfunction(request_user, serialziers_label):
            Adds a new labelfunction.

        - delete_labelfunction(labelfunction_id):
            Deletes a labelfunction by its ID.

        - update_labelfunction(labelfunction_id, request_data):
            Updates a labelfunction by its ID.

        - update_import_labels(workflow_id, request_data, type):
            Updates the labelfunction of the type import or labels for a specified workflow.

        - computeLabels(code, file_path, imports, labels_code, name):
            Gets the labels for a given dataset using the labelfunction from type labels.
    """

    def get_import_labels(self, workflow_id, type):
        """
        Gets a Labelfunction of type import or labels of a specific workflow.

        Args:
            workflow_id (int): The ID of the workflow.
            type (string): The specific type of the labelfunction.

        Returns:
            - int: A HTTP status code.
            - success: The labelfunction object of type import or labels.
            - error: A dictionary containing a error message.
        """
        labelfunction = Labelfunction.objects.filter(workflow_id=workflow_id, type=type)
        if labelfunction.exists():
            serialziers_label = LabelfunctionSerializer(labelfunction[0])
            return status.HTTP_200_OK, serialziers_label.data
        return status.HTTP_404_NOT_FOUND, {"message": f"{type} don't exists"}

    def get_labels(self, workflow_id):
        """
        Retrieves a Labelfunction of type labels of a specific workflow.

        Args:
            workflow_id (int): The ID of the workflow.

        Returns:
            - int: A HTTP status code.
            - success: The labelfunction object of type labels.
            - error: A dictionary containing a error message.
        """
        labelfunction = Labelfunction.objects.filter(
            workflow_id=workflow_id, type="labels"
        )
        if labelfunction.exists():
            serialziers_label = LabelfunctionSerializer(labelfunction[0])
            return status.HTTP_200_OK, serialziers_label.data
        return status.HTTP_404_NOT_FOUND, {"message": "Labels don't exists"}

    def __check_labels(self, workflow_id, L_train_list, L_unlabeled_list):
        """
        Checks whether the returned value of a labelfunction match the labels
        that the creator requires. If not, the labelfunction cannot be created.

        Args:
            workflow_id (int): The ID of the workflow.
            L_train_list (list): Values assigned to a data point in the unlabelled dataset.
            L_unlabeled_list (list): Values assigned to a data point in the train dataset.

        Returns:
            - error: A error message containing the label which is not allowed
        """
        labelfunction_filter = Labelfunction.objects.filter(
            workflow_id=workflow_id, type="labels"
        )
        if labelfunction_filter.exists():
            labelfunction_object_code = labelfunction_filter[0].code
            labels_split = labelfunction_object_code.split()
            labels_split.remove("=")
            while "=" in labels_split:
                labels_split.remove("=")
            L_train_list.extend(L_unlabeled_list)

            for el in L_train_list:
                if str(el) not in labels_split:
                    raise ValueError(
                        f"The label { el } was not spezified by the workflow creator"
                    )

    def count_labels(self, workflow_id):
        labelfunction_filter = Labelfunction.objects.filter(
            workflow_id=workflow_id, type="labels"
        )
        count = 0
        if labelfunction_filter.exists():
            labelfunction_object_code = labelfunction_filter[0].code
            labels_split = labelfunction_object_code.split()
            while "=" in labels_split:
                labels_split.remove("=")
                count = count + 1
        return count - 1

    def compile_labelfunction(self, workflow_id, code):
        """
        Compiled the code of a Labelfunction.

        Args:
            workflow_id (int): The ID of the workflow.
            code (string): The python code a labelfunction.

        Returns:
            - int: A HTTP status code.
            - dict: A dictionary containing a error or success message.
        """
        imports = Labelfunction.objects.filter(workflow_id=workflow_id, type="import")

        if imports.exists():
            import_code = imports[0].code
            try:
                exec(import_code, locals())
                validate_labelfunction(code)
                exec(code, locals())
                return status.HTTP_200_OK, {"message": "The labelfunction compiled"}
            except:
                data = str(sys.exc_info())
                return status.HTTP_400_BAD_REQUEST, data
        return status.HTTP_404_NOT_FOUND, {
            "message": "No import statements where found. from snorkel.labeling import labeling_function needs to be imported"
        }

    def test_labelfunction(self, workflow_id, code, name):
        """
        Gets a Labelfunction of type import or labels of a specific workflow.

        Args:
            workflow_id (int): The ID of the workflow.
            code (string): The python code of a labelfunction.
            name (string): The functionname of a labelfunction.

        Returns:
            - int: A HTTP status code.
            - success: Returns the metrics of the unlabeld and training set
                       and their preictions.
            - error: A dictionary containing a error message.
        """
        file = File.objects.filter(workflow_id=workflow_id)

        if file.exists():
            file_name = file[0].__str__()
            file_path = "{root}/{name}".format(root=MEDIA_ROOT, name=file_name)

            imports = Labelfunction.objects.filter(
                workflow_id=workflow_id, type="import"
            )
            if imports.exists():
                labels = Labelfunction.objects.filter(
                    workflow_id=workflow_id, type="labels"
                )
                if labels.exists():
                    labels_code = labels[0].code
                    return self.__test_on_dataset(
                        code, file_path, imports, name, workflow_id, labels_code
                    )
                return self.__test_on_dataset(
                    code, file_path, imports, name, workflow_id
                )
            return status.HTTP_404_NOT_FOUND, {
                "message": "No import statements where found. from snorkel.labeling import labeling_function needs to be imported"
            }
        return status.HTTP_404_NOT_FOUND, {"message": "No data set has been uploaded"}

    def __test_on_dataset(
        self, code, file_path, imports, name, workflow_id, labels_code=""
    ):
        """
        Gets a Labelfunction of type import or labels of a specific workflow.

        Args:
            code (str): The code of the labelfunction.
            file_path (str): The path to the dataset file.
            imports (QuerySet): The labelfunction of type import.
            name (str): The name of the labelfunction.
            workflow_id (int): The ID of the workflow.
            labels_code (str): The code of the labelfunction of type labels.

        Returns:
            - int: A HTTP status code.
            - success: Returns the metrics of the unlabeld and training set
                       and their preictions.
            - error: A dictionary containing a error message.
        """
        try:
            (
                l_train,
                l_unlabeled,
                dataframe_train,
                dataframe_unlabeled,
                text_list_train_gold_labels,
                lfs,
            ) = self.compute_labels(code, file_path, imports, labels_code, name)

            df_combined = self.__get_datapoints_with_labels(
                l_train, l_unlabeled, dataframe_train, dataframe_unlabeled
            )

            l_train_list = np.array(l_train).flatten().tolist()
            l_unlabeled_list = np.array(l_unlabeled).flatten().tolist()
            self.__check_labels(workflow_id, l_train_list, l_unlabeled_list)
            labelsummary_unlabeled = LFAnalysis(L=l_unlabeled, lfs=lfs).lf_summary()
            labelsummary_train = LFAnalysis(L=l_train, lfs=lfs).lf_summary(
                Y=text_list_train_gold_labels
            )
            labelsummary_unlabeled["index"] = labelsummary_unlabeled.index
            labelsummary_train = labelsummary_train.rename(
                columns={"Emp. Acc.": "EmpAcc"}
            )
            labelsummary_train["index"] = labelsummary_train.index
            return status.HTTP_200_OK, {
                "summary": labelsummary_unlabeled,
                "summary_train": labelsummary_train,
                "df_combined": df_combined,
            }
        except:
            data = str(sys.exc_info())
            return status.HTTP_400_BAD_REQUEST, data

    def __get_datapoints_with_labels(
        self, l_train, l_unlabeled, dataframe_train, dataframe_unlabeled
    ):
        """
        Combines datapoints with their computed labels.

        Args:
            l_train (ndarray): Label predictions of the train dataset.
            l_unlabeled (ndarray): Label predictions of the unlabeled dataset.
            dataframe_train (DataFrame): Training data.
            dataframe_unlabeled (DataFrame): Unlabeled data.

        Returns:
            list: A list of combined data points with their assigned labels.
        """
        dataframe_train["computed_Labels"] = l_train.flatten().tolist()

        dataframe_unlabeled["computed_Labels"] = l_unlabeled.flatten().tolist()

        dataframe_unlabeled = dataframe_unlabeled[
            ["entity_id", "corpus_id", "text", "splitting_id", "computed_Labels"]
        ]
        dataframe_train = dataframe_train[
            [
                "entity_id",
                "corpus_id",
                "text",
                "splitting_id",
                "computed_Labels",
                "class",
            ]
        ]

        df_combined = pd.concat(
            [dataframe_train, dataframe_unlabeled], ignore_index=True
        )
        df_combined = df_combined.fillna("")
        df_combined["index"] = df_combined.index

        data_list = []
        for index, row in df_combined.iterrows():
            data_list.append(
                {
                    "index": index,
                    "entity_id": row["entity_id"],
                    "corpus_id": row["corpus_id"],
                    "text": row["text"],
                    "splitting_id": row["splitting_id"],
                    "computed_Labels": row["computed_Labels"],
                    "class": row["class"],
                }
            )

        return data_list

    def get_all_labelfunction_by_workflow_id(self, workflow_id):
        """
        Retrieves all Labelfunction of a specific workflow.

        Args:
            workflow_id (int): The ID of the workflow.

        Returns:
            - int: A HTTP status code.
            - list: The labelfunction objects as a list.
        """
        labelfunction = (
            Labelfunction.objects.filter(workflow_id=workflow_id)
            .exclude(type="import")
            .exclude(type="labels")
            .order_by("creator")
        )
        serialziers_label = LabelfunctionSerializer(labelfunction, many=True)
        return status.HTTP_200_OK, serialziers_label.data

    def get_labelfunction_by_id(self, labelfunction_id):
        """
        Retrieves a specific Labelfunction by its ID.

        Args:
            labelfunction_id (int): The ID of the labelfunction.

        Returns:
            - int: A HTTP status code.
            - success: The labelfunction object.
            - error: A dictionary containing a error message.
        """
        labelfunction = Labelfunction.objects.filter(pk=labelfunction_id)
        if labelfunction.exists():
            serialziers_label = LabelfunctionSerializer(labelfunction[0])
            return status.HTTP_200_OK, serialziers_label.data
        return status.HTTP_404_NOT_FOUND, {
            "message": "The labelfunction does not exist"
        }

    def add_labelfunction(self, request_user, serialziers_label):
        """
        Add a Labelfunction to a specific workflow.

        Args:
            request_user (User): The ID of the workflow.
            serialziers_label (Serializer): The serialized data of the labelfunction.

        Returns:
            - int: A HTTP status code.
            - success: The id of the created labelfunction.
            - error: A dictionary containing a error message.
        """
        if serialziers_label.is_valid():
            labelfunction = serialziers_label.save(creator=request_user)
            return status.HTTP_201_CREATED, {"lid": labelfunction.id}
        return status.HTTP_400_BAD_REQUEST, serialziers_label.errors

    def delete_labelfunction(self, labelfunction_id):
        """
        Delete a Labelfunction of a specific workflow.

        Args:
            labelfunction_id (int): The ID of the labelfunction.

        Returns:
            - int: A HTTP status code.
            - dict: A dictionary containing a error or success message.
        """
        labelfunction = Labelfunction.objects.filter(pk=labelfunction_id)
        if labelfunction.exists():
            labelfunktion_object = labelfunction[0]
            if (
                not Run.objects.filter(workflow_id=labelfunktion_object.workflow_id)
                .filter(labelfunctions__in=[labelfunktion_object])
                .exists()
            ):
                labelfunktion_object.delete()
                return status.HTTP_200_OK, {
                    "message": "The labelfunction was successfully created"
                }
            return status.HTTP_400_BAD_REQUEST, {
                "message": "The labelfunction can not be deleted as long as it is used in a run."
            }
        return status.HTTP_404_NOT_FOUND, {
            "message": "The labelfunction does not exist"
        }

    def update_labelfunction(self, labelfunction_id, request_data):
        """
        Uodates a Labelfunction of a specific workflow.

        Args:
            labelfunction_id (int): The ID of the labelfunction.
            request_data (dict): The labelfunction object to be updated.

        Returns:
            - int: A HTTP status code.
            - success: The id of the updated labelfunction.
            - error: A dictionary containing a error message.
        """
        labelfunction = Labelfunction.objects.filter(pk=labelfunction_id)
        if labelfunction.exists():
            labelfunktion_object = labelfunction[0]
            serialziers_label = LabelfunctionCreateSerializer(
                labelfunktion_object, data=request_data, partial=True
            )
            if serialziers_label.is_valid():
                labelfunction_updated = serialziers_label.save()
                return status.HTTP_200_OK, {"lid": labelfunction_updated.id}
            return status.HTTP_400_BAD_REQUEST, serialziers_label.errors
        return status.HTTP_404_NOT_FOUND, {
            "message": "The labelfunction does not exist"
        }

    def update_import_labels(self, workflow_id, request_data, type):
        """
        Uodates a Labelfunction of a specific workflow of the type import or labels.

        Args:
            workflow_id (int): The ID of the workflow.
            type (string): The specific type of the labelfunction.
            request_data (dict): The labelfunction object to be updated.

        Returns:
            - int: A HTTP status code.
            - dict: A dictionary containing a error or success message.
        """
        labelfunction_filter = Labelfunction.objects.filter(
            workflow_id=workflow_id, type=type
        )
        if labelfunction_filter.exists():
            import_object = labelfunction_filter[0]
            try:
                import_code = request_data["code"]
                validate_code_for_imports_only(import_code)
                execute_code_in_safe_env(import_code)
                serialziers_import = LabelfunctionCreateSerializer(
                    import_object, data=request_data, partial=True
                )
                if serialziers_import.is_valid():
                    serialziers_import.save()
                    return status.HTTP_200_OK, {
                        "message": f"The {type} were successfully updated"
                    }
                return status.HTTP_400_BAD_REQUEST, serialziers_import.errors
            except:
                data = str(sys.exc_info())
                return status.HTTP_400_BAD_REQUEST, data
        try:
            import_code = request_data["code"]
            exec(import_code, locals())
            serialziers_import = LabelfunctionCreateSerializer(data=request_data)
            if serialziers_import.is_valid():
                serialziers_import.save()
                return status.HTTP_200_OK, {
                    "message": f"The {type} were successfully created"
                }
            return status.HTTP_400_BAD_REQUEST, serialziers_import.errors
        except:
            data = str(sys.exc_info())
            return status.HTTP_400_BAD_REQUEST, data

    def compute_labels(self, code, file_path, imports, labels_code, name):
        """
        Commputes the labels of the datapoints.

        Args:
            l_train (ndarray): Label predictions of the train dataset.
            l_unlabeled (ndarray): Label predictions of the unlabeled dataset.
            dataframe_train (DataFrame): Training data.
            dataframe_unlabeled (DataFrame): Unlabeled data.

        Returns:
            list: A list of combined data points with labels.
        """
        import_code = imports[0].code
        exec(import_code, locals())
        exec(labels_code, locals())
        validate_labelfunction(code)
        exec(code, locals())
        dataframe = pd.read_csv(file_path)
        dataframe_unlabeled = dataframe.loc[(dataframe["splitting_id"] == "unlabeled")]
        dataframe_train = dataframe.loc[(dataframe["splitting_id"] == "train")]
        text_list_train_gold_labels = np.array(dataframe_train["class"].tolist())
        local_var = locals()
        lfs = [local_var[name]]
        with queries_disabled():
            applier = PandasLFApplier(lfs=lfs)
            l_unlabeled = applier.apply(df=dataframe_unlabeled)
            l_train = applier.apply(df=dataframe_train)
        return (
            l_train,
            l_unlabeled,
            dataframe_train,
            dataframe_unlabeled,
            text_list_train_gold_labels,
            lfs,
        )
