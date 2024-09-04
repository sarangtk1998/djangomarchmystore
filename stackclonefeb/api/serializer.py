

from rest_framework import serializers

from django.contrib.auth.models import User
from api.models import Questions,Answers

class UserSerializer(serializers.ModelSerializer):

    class Meta:

        model = User
        fields = ["username",'email','password']

    
    def create(self, validated_data):

        return User.objects.create_user(**validated_data)



class AnswerSerializer(serializers.ModelSerializer):

    id = serializers.CharField(read_only=True)
    user = serializers.CharField(read_only=True)
    question = serializers.CharField(read_only=True)
    # upvote = serializers.CharField(read_only=True)
    upvote_count = serializers.CharField(read_only = True)

    class Meta:

        model = Answers
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):

    user = serializers.CharField(read_only=True)
    date = serializers.CharField(read_only=True)
    question_answer = AnswerSerializer(read_only=True,many=True)

    class Meta:

        model = Questions
        fields = "__all__"