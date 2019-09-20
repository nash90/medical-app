from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request

from ...models import GameBadge
from ...myuser import UserPoints

from ..serializer import BadgeSerializer
from ..serializer import PointsSerializer

class PointsViewSet(APIView):
  permission_classes = [permissions.IsAuthenticatedOrReadOnly]

  def get(self, request, format=None):
    email = request.user

    points = UserPoints.objects.get(user__email=email)
    print(points)
    serializer = PointsSerializer(points)
    return Response(serializer.data)


class BadgeViewSet(viewsets.ModelViewSet):
    queryset = GameBadge.objects.all()
    serializer_class = BadgeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    http_method_names = ['get']