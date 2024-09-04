from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response


class AdditionView(APIView):

    def post(self,request,*args,**kw):

        print(request.data)

        x = int(request.data.get('num1'))
        y = int(request.data.get('num2'))

        z = x+y

        return Response(data=z)