from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render,redirect

# Create your views here.

from django.views.generic import View,TemplateView,ListView,DetailView,CreateView,FormView

from task.forms import TaskForm,RegistrationForm,LoginForm
from task.models import Tasks
from django.urls import reverse_lazy
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages

from django.utils.decorators import method_decorator


def signin_requered(fn):

    def wrapper(request,*args,**kw):

        if not request.user.is_authenticated:

            messages.error(request,"you must login")

            return redirect('signin')
        
        else:
            return fn(request,*args,**kw)
        
    return wrapper
@method_decorator(signin_requered,name="dispatch")  
class TaskCreateViews(CreateView):

    template_name = "task_add.html"
    form_class = TaskForm
    success_url = reverse_lazy('task-list')

    def form_valid(self,form):
        form.instance.user = self.request.user
        messages.success(self.request,"task has been added")
        return super().form_valid(form)

    # def post(self,request,*args,**kw):

    #     form = TaskForm(request.POST)

    #     if form.is_valid():
    #         task = form.save(commit=False)
    #         task.user = request.user
    #         task.save()
    #         return redirect("task-list")
    #     else:
    #         return render(request,"task_add.html",{"form":form})

    # def get(self,request,*args,**kw):

    #     form = TaskForm()

    #     return render(request,"task_add.html",{"form":form})
    

    # def post(self,request,*args,**kw):

    #     form = TaskForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return redirect("task_create")
    #     else:
    #         return render(request,"task_add.html",{"form":form})
@method_decorator(signin_requered,name="dispatch")  
class TaskListView(ListView):

    # def get(self,request,*args,**kw):

    #     qs = Tasks.objects.all()

    #     return render(request,"task_list.html",{"todos":qs})

    model = Tasks
    template_name = 'task_list.html'
    context_object_name = "todos"

    # def get(self,request,*args,**kw):

    #     qs = Tasks.objects.filter(user=request.user)

    #     return render(request,"task_list.html",{"todos":qs})

    def get_queryset(self):
        return Tasks.objects.filter(user=self.request.user)


@method_decorator(signin_requered,name="dispatch")  
class TaskDetailView(DetailView):

    model = Tasks
    template_name = 'task-details.html'
    context_object_name = "todo"
    pk_url_kwarg = "id"

    # def get(self,request,*args,**kw):

    #     id = kw.get("id")

    #     qs = Tasks.objects.get(id=id)

    #     return render(request,"task-details.html",{"todo":qs})
@method_decorator(signin_requered,name="dispatch")  
class TaskDeleteView(View):

    def get(self,request,*args,**kw):

        id = kw.get("id")

        Tasks.objects.get(id=id).delete()
        messages.success(request,"task successfully removed")

        return redirect('task-list')

@method_decorator(signin_requered,name="dispatch")  
class IndexView(TemplateView):

    template_name = "index.html"

class SignUpView(CreateView):

    template_name = 'register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy("signin")

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        messages.success(self.request,"account has been created")
        return super().form_valid(form)


class LoginView(FormView):

    template_name = "login.html"
    form_class = LoginForm
    success_url = reverse_lazy("home")

    def post(self,request,*args,**kw):

        form = LoginForm(request.POST)
        if form.is_valid():

            uname = form.cleaned_data.get('username')
            pwd = form.cleaned_data.get('password')

            usr = authenticate(request,username=uname,password=pwd)

            if usr :
                login(request,usr)
                return redirect("home")
            
            else:
                return render(request,"login.html",{"form":form})
            

def sign_out(request,*args,**kw):

    logout(request)

    return redirect("signin")


# class SignoutView(View):

#     def get(self,request,*args,**kw):

#         logout(request)

#         return redirect("signin")