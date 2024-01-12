from django.contrib import admin
from django.urls import path
from sapper import views

urlpatterns = [
    path('', views.main, name='main_sapper'),
    path('setting', views.setting),
]

