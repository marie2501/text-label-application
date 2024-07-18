import json

from snorkel.labeling.model import MajorityLabelVoter
import numpy as np
from snorkel.labeling.model import LabelModel

from rest_framework import status
from workflow_settings.models import Run, LabelSummary
from workflow_settings.serializers.serializers_run import LabelModelSerializer


class LabelModelService:

    def get_labelmodel_by_run_id(self, run_id):
        run_filter = Run.objects.filter(pk=run_id)
        if run_filter.exists():
            run_object = run_filter[0]
            labelmodel_serializer = LabelModelSerializer(data=run_object.labelmodel)
            return status.HTTP_200_OK, labelmodel_serializer.data
        return status.HTTP_404_NOT_FOUND, {"message": "Run object doesn't exists"}

    # todo speichere cardinality mit in der datenbank, n_epochs... selber wählen -> Referenz welche klassen es gibt
    def label_model(self, run_object, selectedModelLabel, selectedTie, n_epochs=100, log_freq=10, seed=123,
                          base_learning_rate=0.01, l2=0.0, numbers_of_labels=2):
        if selectedModelLabel == 'Majority Vote':
            label = LabelSummary.objects.get_or_create(type='M')
            run_object.labelmodel = label[0]
            run_object.save()
            return self.__majority_vote_label(run_object, numbers_of_labels, selectedTie)
        elif selectedModelLabel == 'Train Label Model':
            label = LabelSummary.objects.get_or_create(type='P')
            run_object.labelmodel = label[0]
            run_object.save()
            return self.__train_label_model(base_learning_rate, l2, log_freq, n_epochs, run_object, seed, numbers_of_labels, selectedTie)
        return {"message": "Choose a valid label service"}

    def __train_label_model(self, base_learning_rate, l2, log_freq, n_epochs, run_object, seed, numbers_of_labels, selectedTie):
        label_model = LabelModel(cardinality=numbers_of_labels, verbose=True)
        labelmatrix_json = json.loads(run_object.labelmatrix)
        labelmatrix = np.array(labelmatrix_json)
        label_model.fit(L_train=labelmatrix, n_epochs=n_epochs, log_freq=log_freq,
                        seed=seed, lr=base_learning_rate, l2=l2)
        preds_unlabeled = label_model.predict(L=labelmatrix, tie_break_policy=selectedTie)
        return preds_unlabeled

    def __majority_vote_label(self, run_object, numbers_of_labels, selectedTie):
        majority_model = MajorityLabelVoter(cardinality=numbers_of_labels)
        labelmatrix_json = json.loads(run_object.labelmatrix)
        labelmatrix = np.array(labelmatrix_json)
        preds_unlabeled = majority_model.predict(L=labelmatrix, tie_break_policy=selectedTie)
        return preds_unlabeled


