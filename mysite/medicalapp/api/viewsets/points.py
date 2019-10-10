"""
# Might be useful if Badge function is implemented in future

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request

#from ...models import GameBadge

#from ..serializer import BadgeSerializer


class BadgeViewSet(viewsets.ModelViewSet):
    queryset = GameBadge.objects.all()
    serializer_class = BadgeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    http_method_names = ['get']
"""    