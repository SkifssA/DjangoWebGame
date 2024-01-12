from django.contrib import admin
from django.urls import path
from Game import views

urlpatterns = [
    path('game&=<int:key_id>', views.game, name='game'),
    path('', views.show_all_img, name='all_img'),
    path('uploadIMG', views.upload_img, name='upload'),
]

