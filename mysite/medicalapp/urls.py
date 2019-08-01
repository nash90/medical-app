from django.conf.urls import url, include
from django.urls import path
from rest_framework import routers

from . import views
from .api.viewset import DrugViewSet

router = routers.DefaultRouter()
router.register(r'api/drugs', DrugViewSet)

urlpatterns = [
    path('', views.index, name='index'),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))  
]
