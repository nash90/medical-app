import random
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import renderers
from django.conf import settings

from ...models import DrugKeyword
from ...myuser import Profile

from ..serializer import DrugKeywordSerializer
from ..serializer import GameKeywordSerializer

class KeywordViewSet(viewsets.ModelViewSet):
    queryset = DrugKeyword.objects.all()
    serializer_class = DrugKeywordSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    http_method_names = ['get']

    @action(detail=True)
    def game(self, request, pk=0):
        keyword = DrugKeyword.objects.get(keyword_id=pk)
        data = {
            "keyword": keyword,
            "game_keyword": keywordScrabble(keyword.keyword)
        }
        
        serializer = GameKeywordSerializer(data)
        return Response(serializer.data)

    @action(detail=True)
    def answer(self, request, pk=0):
        user = request.user
        params = request.query_params
        answer = params["answer"]
        res = {
            "correct":False
        }
        if(answer != None):
            keyword_obj = DrugKeyword.objects.get(keyword_id=pk)
            if (answer.lower() == keyword_obj.keyword.lower()):
                res["correct"] = True
                updatePoints(user)
        return Response(res)



### Helper Functions
def keywordScrabble(keyword):
    new_key = ""
    for item in keyword:
        a = random.choice([True, False])
        if item != " " and a == False:
            new_key = new_key + "*"
        else:
            new_key = new_key + item
    return new_key

def updatePoints(user):
    profile = Profile.objects.get(user__email=user)
    current_points = profile.points
    correct_points = settings.DEFAULT_QUIZ_POINT
    if current_points == None:
        profile.points = correct_points
        profile.save()
    else:
        profile.points = current_points + correct_points
        profile.save()