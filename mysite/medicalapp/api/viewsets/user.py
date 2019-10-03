import random
from django import forms
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import renderers
from django.shortcuts import get_object_or_404
from rest_framework_jwt.views import ObtainJSONWebToken

from django.contrib import auth
User = auth.get_user_model()
from ...myuser import Profile

from ..serializer import ProfileSerializer
from ..serializer import JWTSerializer

class UserViewSet(APIView):
  authentication_classes = []
  queryset = User.objects.all()
  permission_classes = [permissions.AllowAny]
  def post(self, request, format=None):
    serializer = ProfileSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
      serializer.save()
      return Response(serializer.data)
    else:
      return Response(serializer.errors)

class ObtainJWTView(ObtainJSONWebToken):
    serializer_class = JWTSerializer

class UserProfileViewSet(APIView):
  permission_classes = [permissions.IsAuthenticatedOrReadOnly]

  def get(self, request, format=None):
    email = request.user
    #print(email)
    profile = None
    try:
      profile = Profile.objects.get(user__email=email)
    except Exception as e:
      print(e)
    if profile != None:
      serializer = ProfileSerializer(profile)
      return Response(serializer.data)
    else:
      return Response('Profile does not exist')


    