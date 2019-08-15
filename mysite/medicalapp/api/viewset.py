import random
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import renderers

from ..models import Drug
from ..models import DrugInformation
from ..models import DrugKeyword

from .serializer import DrugSerializer
from .serializer import DrugInfoSerializer
from .serializer import DrugKeywordSerializer
from .serializer import GameKeywordSerializer

class DrugViewSet(viewsets.ModelViewSet):
    queryset = Drug.objects.all()
    serializer_class = DrugSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    http_method_names = ['get']

    @action(detail=False)
    def custom(self, request):
        data = Drug.objects.all()
        serializer = DrugSerializer(data, many=True)
        return Response(serializer.data)

    @action(detail=True)
    def info(self, request, pk=0):
        data = DrugInformation.objects.filter(drug__drug_id=pk)
        serializer = DrugInfoSerializer(data, many=True)
        return Response(serializer.data)   
    
    @action(detail=True)
    def gameinfo(self, request, pk=0):
        data = DrugInformation.objects.filter(drug__drug_id=pk)
        serializer = DrugInfoSerializer(data, many=True)
        return Response(serializer.data)

class DrugInfoViewSet(viewsets.GenericViewSet):
    queryset = DrugInformation.objects.all()
    serializer_class = DrugInfoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    http_method_names = ['get']

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
        params = request.query_params
        answer = params["answer"]
        res = {
            "correct":False
        }
        if(answer != None):
            keyword_obj = DrugKeyword.objects.get(keyword_id=pk)
            if (answer.lower() == keyword_obj.keyword.lower()):
                res["correct"] = True
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