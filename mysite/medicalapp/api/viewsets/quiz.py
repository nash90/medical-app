import random
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import renderers

from django.conf import settings

from ...models import DrugQuizQuestion
from ...models import DrugQuizOption
from ...myuser import Profile

from ..serializer import DrugQuizSerializer
from ..serializer import DrugQuizDetailSerializer
from ..serializer import QuizAnswerSerializer

class DrugQuizViewSet(viewsets.ViewSet):
    queryset = DrugQuizQuestion.objects.all()
    serializer_class = DrugQuizSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    http_method_names = ['get']

    @action(detail=True)
    def info(self, request, pk=0):
        """
        Api Handler to get quiz information by id,
        returns a quiz and its option
        """
        drug_quiz = DrugQuizQuestion.objects.get(drug_quiz_id=pk)
        quiz_option = DrugQuizOption.objects.filter(quiz__drug_quiz_id=pk)
        quiz_option = list(quiz_option)
        random.shuffle(quiz_option)        
        data = {
            "drug_quiz": drug_quiz,
            "quiz_option": quiz_option
        }
        
        serializer = DrugQuizDetailSerializer(data)
        return Response(serializer.data)

    @action(detail=False)
    def filter(self, request):
        """
        Api Handler to get quizes information by drug id, drug_info_type, quiz_type
        returns a list of quiz and its option        
        """
        params = request.query_params
        drug = params.get("drug", 0)
        drug_info_type = params.get("drug_info_type", 0)
        quiz_type = params.get("quiz_type", "Level")
        if quiz_type == "End":
            drug_quiz = DrugQuizQuestion.objects.filter(drug__drug_id = drug).filter(quiz_type = quiz_type)
        else:
            drug_quiz = DrugQuizQuestion.objects.filter(
                    drug__drug_id = drug
                ).filter(
                    drug_info_type__drug_info_type_id = drug_info_type
                ).filter(
                    quiz_type = quiz_type
                )

        data_list = []
        for item in drug_quiz:
            quiz_option =  DrugQuizOption.objects.filter(quiz__drug_quiz_id=item.drug_quiz_id)
            quiz_option = list(quiz_option)
            random.shuffle(quiz_option)
            data = {
            "drug_quiz": item,
            "quiz_option": quiz_option
            }
            data_list.append(data)  

        serializer = DrugQuizDetailSerializer(data_list, many=True)
        return Response(serializer.data)

    @action(detail=True)
    def answer(self, request, pk=0):
        """
        check answer of quiz one by one
        not used after the bulk answer check was implemented
        """
        params = request.query_params
        answer = int(params.get("option", 0))
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
        """
        Api handler for checking answer of a quiz in bulk
        """
        user = request.user
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

                correct_id = 0
                if len(correct_answer) > 0:
                    correct_answer = correct_answer[0]
                    correct_id = correct_answer.quiz_option_id
                
                if (correct_id) == answer:
                    res["correct"] = True
                    updatePoints(user)
                else:
                    wrong_answer = DrugQuizOption.objects.get(quiz_option_id=answer)
                    res["message"] = wrong_answer.rational
                    if res["message"] == "NaN":
                        res["message"] = ""
                res["correct_option_id"] = correct_id
                result.append(res)
              
        return Response(result)

## helper methods

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
