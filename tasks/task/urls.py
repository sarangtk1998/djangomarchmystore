
from django.urls import path
from task import views

urlpatterns = [
    path('task/add',views.TaskCreateViews.as_view(),name='task_create'),
    path("tasks/all",views.TaskListView.as_view(),name="task-list"),
    path("task/<int:id>/",views.TaskDetailView.as_view(),name="task-detail"),
    path("task/<int:id>/remove",views.TaskDeleteView.as_view(),name="task-delete"),
    path("index",views.IndexView.as_view(),name='home'),
    path("register",views.SignUpView.as_view(),name="signup"),
    path("",views.LoginView.as_view(),name='signin'),
    path("logout",views.sign_out,name="logout")
]
