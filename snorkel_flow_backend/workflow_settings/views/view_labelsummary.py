from rest_framework import status, authentication, viewsets
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from workflow_settings.models import Run


class LabelView(viewsets.ViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated]
    parser_class = [JSONParser]

    def getLabelModel(self, request, *args, **kwargs):
        run_id = kwargs['pk']
        run = Run.objects.filter(pk=run_id)
        if run.exists():
            run = run[0]
            if run.labelsummary.objects.exists():
                data = {'type': run.labelsummary.type}
                return Response(data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)
