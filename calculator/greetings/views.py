from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime


class GoodmorningView(APIView):

    def get(self,request,*args,**kw):

        return Response(data='hello good morning')
    

class TodayView(APIView):

    def get(self,request,*args,**kw):

        date = datetime.today()

        return Response(data=date)


class TimeView(APIView):

    def get(self,request,*args,**kw):

        time = datetime.now()

        return Response(data=time)
