from rest_framework import serializers
from django.contrib.auth import authenticate, user_logged_in
from rest_framework_jwt.serializers import JSONWebTokenSerializer, jwt_payload_handler, jwt_encode_handler
from django.contrib.auth import hashers

from django.conf import settings

from django.contrib import auth
User = auth.get_user_model()
from ..models import DrugClass
from ..models import DrugSubClass
from ..models import DrugInformationType
from ..models import Drug
from ..models import DrugInformation
from ..models import DrugKeyword
from ..models import DrugQuizQuestion
from ..models import DrugQuizOption
from ..myuser import Profile
#from ..models import GameBadge

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

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    # badge = GameBadge()

    class Meta:
        model = Profile
        fields = ['date_of_birth', 'user', 'points']
    
    def create(self, validated_data):
        user_form = validated_data['user']
        user = User.objects.create(
            email = user_form['email'],
            # password = hashers.make_password(user_form['password']) # Stakeholder wanted login without PW
        )
        Profile.objects.create(
            user=user, 
            date_of_birth = validated_data['date_of_birth']
            )
        return validated_data

class JWTSerializer(JSONWebTokenSerializer):
    password = serializers.CharField(required=False)
    year_of_birth = serializers.CharField(required=True) 

    def validate(self, attrs):
        credentials = {
            self.username_field: attrs.get(self.username_field),
            # 'password' : attrs.get('password') # Stakeholder wanted login without PW      
        }

        if all(credentials.values()):
            # user = authenticate(request=self.context['request'], **credentials) # used if password login active
            user = User.objects.get(email = attrs.get(self.username_field))

            if user:
                if not user.is_active:
                    msg = 'User account is disabled.'
                    raise serializers.ValidationError(msg)
                profile = Profile.objects.get(user_id = user.id)

                if str(profile.date_of_birth.year) != attrs.get('year_of_birth'):
                    msg = 'Incorrect login information provided'
                    raise serializers.ValidationError(msg)

                payload = jwt_payload_handler(user)
                user_logged_in.send(sender=user.__class__, request=self.context['request'], user=user)

                return {
                    'token': jwt_encode_handler(payload),
                    'user': user
                }
            else:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg)
        else:
            msg = 'Must include "{username_field}" and "password".'
            msg = msg.format(username_field=self.username_field)
            raise serializers.ValidationError(msg)

class QuizAnswerSerializer(serializers.Serializer):
    quiz_id = serializers.IntegerField(required=True)
    answer = serializers.IntegerField(required=True)

"""
class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameBadge
        fields = ['badge_id', 'rank', 'name', 'points']
"""