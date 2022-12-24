
from re import I
from unicodedata import name
from django import views
from django.contrib import admin
from django.urls import path
from . views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', TaskList.as_view() , name= 'home' ),
    path('details/<int:pk>/', TaskDetail.as_view(), name='details' ),
    path('create-task/', CreateTask.as_view() , name= 'create-task' ),
    path('update/<int:pk>/', UpdateTask.as_view() , name= 'update-task' ),
    path('delete/<int:pk>/', DeleteTask.as_view() , name= 'delete-task' ),
    path('login/' , CustomLogin.as_view(), name='login'),
    path('register/' , RegisterUser.as_view(), name='register'),
    path('logout/' , LogoutView.as_view(next_page= 'login'), name='logout'),

]