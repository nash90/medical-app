from django.conf.urls import url, include
from django.urls import path
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

from . import views
from .api.viewset import DrugViewSet
from .api.viewset import DrugInfoViewSet
from .api.viewset import KeywordViewSet
from .api.quizviewset import DrugQuizViewSet
from .api.quizviewset import AnswerViewSet
from .api.userviewset import UserViewSet
from .api.userviewset import ObtainJWTView
from .api.viewsets.points import PointsViewSet
from .api.viewsets.points import BadgeViewSet
from .api.userviewset import UserProfileViewSet

router = routers.DefaultRouter()
router.register(r'api/drugs', DrugViewSet)
#router.register(r'api/druginfo', DrugInfoViewSet)
router.register(r'api/keys', KeywordViewSet)
router.register(r'api/quiz', DrugQuizViewSet)
router.register(r'api/badge', BadgeViewSet)
#router.register(r'api/user', UserViewSet)

urlpatterns = [
    path('', views.index, name='index'),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path(r'api/login/', ObtainJWTView.as_view()),
    path(r'api-token-refresh/', refresh_jwt_token),
    path(r'api/register/', UserViewSet.as_view()),
    path(r'api/checkans/', AnswerViewSet.as_view()),
    path(r'api/points/', PointsViewSet.as_view()),
    path(r'api/profile/', UserProfileViewSet.as_view()),
]
