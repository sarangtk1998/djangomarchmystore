
from task.models import Tasks
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from django import forms

class TaskForm(forms.ModelForm):

    class Meta:
        model = Tasks
        fields = ["task_name"]

class RegistrationForm(UserCreationForm):

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))

    class Meta:
        model = User
        fields = ["email",'username','password1','password2']

        widgets = {

            "email":forms.EmailInput(attrs={"class":"form-control"}),
            "username":forms.TextInput(attrs={"class":"form-control"})
                   }

class LoginForm(forms.Form):

    username = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))


