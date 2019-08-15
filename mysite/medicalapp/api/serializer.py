from rest_framework import serializers
from ..models import DrugClass
from ..models import DrugSubClass
from ..models import DrugInformationType
from ..models import Drug
from ..models import DrugInformation
from ..models import DrugKeyword
from ..models import DrugQuizQuestion
from ..models import DrugQuizOption

class DrugClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = DrugClass
        fields = ['drug_class_id', 'drug_class_name', 'drug_class_description']  

class DrugSubClassSerializer(serializers.ModelSerializer):
    drug_class = DrugClassSerializer(read_only=True)
    class Meta:
        model = DrugSubClass
        fields = ['drug_subclass_id', 'drug_class' ,'drug_subclass_name', 'drug_subclass_description']          

class DrugInfoTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DrugInformationType
        fields = ['drug_info_type_id', 'drug_information_type', 'game_level']

class DrugSerializer(serializers.HyperlinkedModelSerializer):
    drug_subclass = DrugSubClassSerializer(read_only=True)
    class Meta:
        model = Drug
        fields = ['drug_id', 'drug_subclass', 'drug_name', 'black_box_warning']

class DrugKeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = DrugKeyword
        fields = ['keyword_id', 'keyword']

class DrugInfoSerializer(serializers.ModelSerializer):
    drug = DrugSerializer(read_only=True)
    drug_info_type = DrugInfoTypeSerializer(read_only=True)
    keyword = DrugKeywordSerializer(many=True, read_only=True)
    class Meta:
        model = DrugInformation
        fields = ['drug_info_id', 'drug', 'drug_info_type', 'information', 'scrabble_hint', 'keyword']

class GameKeywordSerializer(serializers.Serializer):
    keyword = DrugKeywordSerializer(read_only=True)
    game_keyword = serializers.CharField(max_length=200)

class DrugQuizOption(serializers.ModelSerializer):
    class Meta:
        model = DrugQuizOption
        fields = ['quiz_option_id', 'quiz_option']

class DrugQuizSerializer(serializers.ModelSerializer):
    drug = DrugSerializer(read_only=True)
    drug_info_type = DrugInfoTypeSerializer(read_only=True)

    class Meta:
        model = DrugQuizQuestion
        fields = ['drug_quiz_id', 'drug', 'drug_info_type', 'quiz_question', 'quiz_type', 'enable']

class DrugQuizDetailSerializer(serializers.Serializer):
    drug_quiz = DrugQuizSerializer(read_only=True)
    quiz_option = DrugQuizOption(many=True, read_only=True)