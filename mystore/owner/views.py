from django.shortcuts import render
from owner.forms import LoginForm,RegistrationForm,ProductForm
from django.contrib.auth.models import User

# Create your views here.

from django.views.generic import View

class HomeView(View):

    def get(self,request,*args,**kw):

        return render(request,"home.html")
    

class SignUpView(View):

    def get(self,request,*args,**kw):

        form = RegistrationForm()

        return render(request,"register.html",{"form":form})
    
    def post(self,request,*args,**kw):

        # print(request.POST)
        # print(request.POST.get("first_name"))

        form = RegistrationForm(request.POST)
        form1 = LoginForm()

        if form.is_valid():

            # form.save()
            User.objects.create_user(**form.cleaned_data)
            return render(request,"login.html",{"form":form1})
        else:
            return render(request,'register.html',{"form":form})

    
class SignInView(View):

    def get(self,request,*args,**kw):

        form = LoginForm()

        return render(request,"login.html",{"form":form})
    
    def post(self,request,*args,**kw):

        print(request.POST)      #{"username":'sarang','password':123456}
        print(request.POST.get("username"))
        print(request.POST.get("password"))

        return render(request,'home.html')
    

class ProductAddView(View):

    def get(self,request,*args,**kw):

        form = ProductForm()

        return render(request,"product-add.html",{"form":form})
    
    def post(self,request,*args,**kw):

        form = ProductForm(request.POST,files=request.FILES)

        if form.is_valid():
            form.save()

            return render(request,"home.html")
        
        else:
            return render(request,"product-add.html",{"form":form})

