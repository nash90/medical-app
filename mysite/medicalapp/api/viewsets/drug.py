import random
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import renderers
from django.conf import settings

from ...models import Drug
from ...models import DrugInformation

from ..serializer import DrugSerializer
from ..serializer import DrugInfoSerializer

class DrugViewSet(viewsets.ModelViewSet):
    queryset = Drug.objects.all()
    serializer_class = DrugSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    http_method_names = ['get']

    @action(detail=True)
    def info(self, request, pk=0):
        """
        Api handler to get all the information related to a drug_id
        """
        data = DrugInformation.objects.filter(drug__drug_id=pk)
        serializer = DrugInfoSerializer(data, many=True)
        return Response(serializer.data)

class DrugInfoViewSet(viewsets.GenericViewSet):
    """
    Not Used at the moment, might be useful if api for modifying druginfo is needed
    """
    queryset = DrugInformation.objects.all()
    serializer_class = DrugInfoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    http_method_names = ['get']
