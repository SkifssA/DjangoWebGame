from django.contrib import admin
from django.urls import path
from TowerDefense import views

urlpatterns = [
    path('', views.main, name='main_td'),
    path('settingPole<str:key>/', views.CellGen.as_view()),
    path('towers<str:key>/', views.Towers.as_view()),
    path('GoOr<int:key>/', views.EnemyGo.as_view()),
]

