"""
URL configuration for mystore project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from api import views

from rest_framework.authtoken.views import ObtainAuthToken

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('api/products',views.ProductModelViewset,basename="products")
router.register("users",views.UserView,basename='users')
router.register('carts',views.CartView,basename='carts')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('products',views.ProductView.as_view()),
    path('products/<int:id>',views.ProductdetailsView.as_view()),
    # path('carts/<int:id>',views.CartView.as_view())
    path('Review/<int:pk>',views.ReviewDeleteView.as_view()),
    path('token',ObtainAuthToken.as_view()),
    path("owner/",include("owner.urls"))
]+router.urls
