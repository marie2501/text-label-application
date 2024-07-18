import pandas as pd
from rest_framework import authentication, viewsets
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from workflow_settings.models import Run
from workflow_settings.permissions import IsRunCreatorPermission
from workflow_settings.services.run_service.classifier_service import ClassiferService
from workflow_settings.services.run_service.run_service import RunService


class ClassiferView(viewsets.ViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated, IsRunCreatorPermission]
    parser_class = [JSONParser]

    # todo get classifier assocatied with the run
    # todo get number of labels automatisch wichtig

    def call_classifier(self, request, *args, **kwargs):
        run_id = kwargs['run_id']
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
        selectedTie = request.data['selectedTie']
        filterAbstain = request.data['filterAbstain']
        # todo get automatically
        numbers_of_labels = 2

        runservice = RunService()
        status, data, L_train_train, dataframe_train, labelfunction_names = runservice.exec_run(run_id)

        classifierservice = ClassiferService()
        status, data, predictions_train = classifierservice.call_classifier(run_id, selectedModelClassifier, selectedModelLabel, selectedModelFeaturize, range_x, range_y, n_epochs, log_freq, seed, base_learning_rate, l2, numbers_of_labels, selectedTie, filterAbstain)


        labelfunctions_dataframe = pd.DataFrame(L_train_train, columns=labelfunction_names)
        if labelfunctions_dataframe.shape[0] == dataframe_train.shape[0]:
            labelfunctions_dataframe = labelfunctions_dataframe.reset_index(drop=True)
            dataframe_train = dataframe_train[['entity_id', 'corpus_id', 'text', 'splitting_id', 'CLASS']]
            dataframe_train = dataframe_train.reset_index(drop=True)
            df_combined = pd.concat([dataframe_train, labelfunctions_dataframe], axis=1)
            df_combined['Classifier_predictions'] = predictions_train
            # df_combined['index'] = df_combined.index
            df_combined = df_combined.fillna('')

            json_dataframe = df_combined.to_dict(orient="split")
            data.update({'df_combined': json_dataframe})

            return Response(data=data, status=status)

        return Response(data=data, status=status)