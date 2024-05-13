from rest_framework import status, authentication, viewsets
from rest_framework.parsers import JSONParser, FileUploadParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from workflow_settings.permissions import IsLabelfuntionCreatorPermission, WorkflowAccessPermission
from workflow_settings.serializers.serializers_labelfunction import LabelfunctionSerializer, LabelfunctionCreateSerializer
from workflow_settings.services.labelfunktion_service.labelfunction_service import LabelfunctionService


class LabelfunctionView(viewsets.ViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated, WorkflowAccessPermission]
    parser_class = [JSONParser]

    def get_import_labels(self, request, *args, **kwargs):
        workflow_id = kwargs['workflow_id']
        type = kwargs['type']

        labelfunction = LabelfunctionService()
        status, data = labelfunction.get_import_labels(workflow_id, type)

        return Response(status=status, data=data)

    def update_import_labels(self, request, *args, **kwargs):
        workflow_id = kwargs['workflow_id']
        request_data = request.data
        type = request.data['type']

        labelfunction = LabelfunctionService()
        status, data = labelfunction.update_import_labels(workflow_id, request_data, type)
        return Response(status=status, data=data)

    def get_all_labelfunction_by_workflow_id(self, request, *args, **kwargs):
        workflow_id = kwargs['workflow_id']

        labelfunction = LabelfunctionService()
        status, data = labelfunction.get_all_labelfunction_by_workflow_id(workflow_id)
        return Response(status=status, data=data)


    def add_labelfunction(self, request, *args, **kwargs):
        workflow_id = kwargs['workflow_id']
        request_data = request.data
        request_data['workflow'] = workflow_id
        labelfunction_code = request.data['code']
        name = request.data['name']

        labelfunction = LabelfunctionService()

        # First step: Compile Pythoncode
        status_c, data_c = labelfunction.compile_labelfunction(workflow_id, labelfunction_code)
        if status_c == status.HTTP_200_OK:
            # Second step: Test Pythoncode on real Dataset
            status_t, data_t = labelfunction.test_labelfunction(workflow_id, labelfunction_code, name)
            # Third step: Save Function
            if status_t == status.HTTP_200_OK:
                request_data['summary_unlabeled'] = data_t['summary'].to_json(orient='split')
                request_data['summary_train'] = data_t['summary_train'].to_json(orient='split')
                serialziers_label = LabelfunctionCreateSerializer(data=request_data)
                status_s, data_s = labelfunction.add_labelfunction(request.user, serialziers_label)
                if status_s == status.HTTP_201_CREATED:
                    data_s.update(data_t)
                return Response(status=status_s, data=data_s)
            return Response(status=status_t, data=data_t)
        return Response(status=status_c, data=data_c)

class LabelfunctionModifyView(viewsets.ViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated, IsLabelfuntionCreatorPermission]
    parser_class = [JSONParser]

    def get_labelfunction_by_id(self, request, *args, **kwargs):
        labelfunction_id = kwargs['labelfunction_id']

        labelfunction = LabelfunctionService()
        status, data = labelfunction.get_labelfunction_by_id(labelfunction_id)

        return Response(status=status, data=data)

    def delete_labelfunction(self, request, *args, **kwargs):
        labelfunction_id = kwargs['labelfunction_id']

        labelfunction = LabelfunctionService()
        status, data = labelfunction.delete_labelfunction(labelfunction_id)
        return Response(status=status, data=data)

    def update_labelfunction(self, request, *args, **kwargs):
        labelfunction_id = kwargs['labelfunction_id']
        request_data = request.data
        workflow_id = request_data['workflow_id']
        labelfunction_obj = request_data['labelfunction']

        labelfunction_service = LabelfunctionService()

        status_c, data_c = labelfunction_service.compile_labelfunction(workflow_id, labelfunction_obj['code'])
        if status_c == status.HTTP_200_OK:
            # Second step: Test Pythoncode on real Dataset
            status_t, data_t = labelfunction_service.test_labelfunction(workflow_id, labelfunction_obj['code'], labelfunction_obj['name'])
            # Third step: Save Function
            if status_t == status.HTTP_200_OK:
                labelfunction_obj['summary_unlabeled'] = data_t['summary'].to_json(orient='split')
                labelfunction_obj['summary_train'] = data_t['summary_train'].to_json(orient='split')
                status_s, data_s = labelfunction_service.update_labelfunction(labelfunction_id, labelfunction_obj)
                if status_s == status.HTTP_200_OK:
                    data_s.update(data_t)
                return Response(status=status_s, data=data_s)
            return Response(status=status_t, data=data_t)
        return Response(status=status_c, data=data_c)
