from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from api.serializer import UserSerializer,QuestionSerializer,AnswerSerializer
from rest_framework.response import Response
from api.models import Questions,Answers
from rest_framework import authentication,permissions
from rest_framework.decorators import action
from rest_framework import serializers

class UserView(viewsets.ViewSet):

    def create(self,request,*args,**kw):

        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save()

            return Response(data=serializer.data)
        
        else:
            return Response(data=serializer.errors)
        

class QuestionView(viewsets.ModelViewSet):

    serializer_class = QuestionSerializer
    queryset = Questions.objects.all()
    # authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):

        serializer = QuestionSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save(user=request.user)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        
    # def list(self, request, *args, **kwargs):

    #     qs = Questions.objects.all().exclude(user=request.user)
    #     serializer = QuestionSerializer(qs,many=True)

    #     return Response(data=serializer.data)

    def get_queryset(self):
        
        return Questions.objects.all().exclude(user=self.request.user)
    

    @action(methods=["POST"],detail=True)
    def add_answer(self, request, *args, **kwargs):

        # id = kwargs.get('pk')
        # object = Questions.objects.get(id=id)

        object = self.get_object()
        user = request.user

        serializer = AnswerSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save(user=user,question=object)

            return Response(data=serializer.data)

        else:
            return Response(data=serializer.errors)


class AnswerView(viewsets.ModelViewSet):

    serializer_class = AnswerSerializer
    queryset = Answers.objects.all()
    # authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):

        raise serializers.ValidationError("method not allowed")
    
    def list(self, request, *args, **kwargs):

        raise serializers.ValidationError("method not allowed")
    
    def destroy(self, request, *args, **kwargs):
       
    #    id = kwargs.get('pk')
    #    object = Answers.objects.get(id=id)

        object = self.get_object()

        if request.user == object.user:
            object.delete()
            return Response(data='answer deleted')
        else:
            raise serializers.ValidationError('permition deneid for this user')
        
    @action(methods=["POST"],detail=True)
    def upvote(self, request, *args, **kwargs):

        object = self.get_object()
        user = request.user
        object.upvote.add(user)

        return Response(data="up voted")

