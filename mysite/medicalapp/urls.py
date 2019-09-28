from django.conf.urls import url, include
from django.urls import path
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

from . import views
from .api.viewsets.drug import DrugViewSet
from .api.viewsets.keyword import KeywordViewSet
from .api.viewsets.quiz import DrugQuizViewSet
from .api.viewsets.quiz import AnswerViewSet
from .api.viewsets.user import UserViewSet
from .api.viewsets.user import ObtainJWTView
from .api.viewsets.user import UserProfileViewSet

router = routers.DefaultRouter()
router.register(r'api/drugs', DrugViewSet)
router.register(r'api/keys', KeywordViewSet)
router.register(r'api/quiz', DrugQuizViewSet)

urlpatterns = [
    path('', views.index, name='index'),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path(r'api/login/', ObtainJWTView.as_view()),
    path(r'api-token-refresh/', refresh_jwt_token),
    path(r'api/register/', UserViewSet.as_view()),
    path(r'api/checkans/', AnswerViewSet.as_view()),
    path(r'api/profile/', UserProfileViewSet.as_view()),
]
