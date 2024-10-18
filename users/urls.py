from django.urls import path
from . import views

userController = views.UserController()

urlpatterns = [
    path('', views.UserController.as_view()),
]