import random
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import renderers

from ..models import DrugQuizQuestion
from ..models import DrugQuizOption

from .serializer import DrugQuizSerializer
from .serializer import DrugQuizDetailSerializer
from .serializer import QuizAnswerSerializer

class DrugQuizViewSet(viewsets.ModelViewSet):
    queryset = DrugQuizQuestion.objects.all()
    serializer_class = DrugQuizSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    http_method_names = ['get']

    @action(detail=True)
    def info(self, request, pk=0):
        drug_quiz = DrugQuizQuestion.objects.get(drug_quiz_id=pk)
        quiz_option = DrugQuizOption.objects.filter(quiz__drug_quiz_id=pk)
        data = {
            "drug_quiz": drug_quiz,
            "quiz_option": quiz_option
        }
        
        serializer = DrugQuizDetailSerializer(data)
        return Response(serializer.data)

    @action(detail=False)
    def filter(self, request):
      params = request.query_params
      drug = params["drug"]
      drug_info_type = params["drug_info_type"]
      drug_quiz = DrugQuizQuestion.objects.filter(drug__drug_id = drug).filter(drug_info_type__drug_info_type_id = drug_info_type)

      data_list = []
      for item in drug_quiz:
        quiz_option =  DrugQuizOption.objects.filter(quiz__drug_quiz_id=item.drug_quiz_id)
        data = {
          "drug_quiz":item,
          "quiz_option":quiz_option
        }
        data_list.append(data)  

      serializer = DrugQuizDetailSerializer(data_list, many=True)
      return Response(serializer.data)

    @action(detail=True)
    def answer(self, request, pk=0):
        params = request.query_params
        answer = int(params["option"])
        res = {
            "correct":False,
            "correct_option_id":None
        }
        if(answer != None):
            correct_answer = DrugQuizOption.objects.filter(quiz__drug_quiz_id=pk).filter(correct_flag=True)
            correct_answer = correct_answer[0]
            correct_id = correct_answer.quiz_option_id
            if (correct_id) == answer:
                res["correct"] = True
            res["correct_option_id"] = correct_id
            
        return Response(res)



class AnswerViewSet(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def post(self, request, format=None):
        serializer = QuizAnswerSerializer(data=request.data, many=True)
        result = []
        if serializer.is_valid():
            #print(serializer)
            for item in serializer.data:
                quiz_id = item['quiz_id']
                answer = item['answer']
                res = {
                    "quiz_id": quiz_id,
                    "answer": answer,
                    "correct":False,
                    "correct_option_id":None,
                    "message":""
                }
                correct_answer = DrugQuizOption.objects.filter(quiz__drug_quiz_id=quiz_id).filter(correct_flag=True)

                correct_answer = correct_answer[0]
                correct_id = correct_answer.quiz_option_id
                if (correct_id) == answer:
                    res["correct"] = True
                else:
                    wrong_answer = DrugQuizOption.objects.get(quiz_option_id=answer)
                    res["message"] = wrong_answer.rational
                res["correct_option_id"] = correct_id
                result.append(res)
              
        return Response(result)