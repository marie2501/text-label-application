from rest_framework import authentication, viewsets
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from workflow_settings.models import Run
from workflow_settings.permissions import IsRunCreatorPermission
from workflow_settings.services.run_service.classifier_service import ClassiferService


class ClassiferView(viewsets.ViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated, IsRunCreatorPermission]
    parser_class = [JSONParser]

    # todo get classifier assocatied with the run

    def call_classifier(self, request, *args, **kwargs):
        run_id = kwargs['run_id']
        run = Run.objects.filter(pk=run_id)
        selectedModelClassifier = request.data['selectedModelClassifier']
        selectedModelLabel = request.data['selectedModelLabel']
        selectedModelFeaturize = request.data['selectedModelFeaturize']
        range_x = request.data['range_x']
        range_y = request.data['range_y']
        n_epochs = request.data['n_epochs']
        log_freq = request.data['log_freq']
        seed = request.data['seed']
        base_learning_rate = request.data['base_learning_rate']
        l2 = request.data['l2']
        numbers_of_labels = 2 #request.data['numbers_of_labels']

        classifierservice = ClassiferService()
        status, data = classifierservice.call_classifier(run_id, selectedModelClassifier, selectedModelLabel, selectedModelFeaturize, range_x, range_y, n_epochs, log_freq, seed, base_learning_rate, l2, numbers_of_labels)

        return Response(data=data, status=status)