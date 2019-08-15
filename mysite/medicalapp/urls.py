from django.conf.urls import url, include
from django.urls import path
from rest_framework import routers

from . import views
from .api.viewset import DrugViewSet
from .api.viewset import DrugInfoViewSet
from .api.viewset import KeywordViewSet
from .api.quizviewset import DrugQuizViewSet

router = routers.DefaultRouter()
router.register(r'api/drugs', DrugViewSet)
#router.register(r'api/druginfo', DrugInfoViewSet)
router.register(r'api/keys', KeywordViewSet)
router.register(r'api/quiz', DrugQuizViewSet)

urlpatterns = [
    path('', views.index, name='index'),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))  
]
