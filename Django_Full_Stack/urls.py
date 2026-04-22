from django.contrib import admin
from django.urls import path
from games import views
urlpatterns = [
    path('', views.home, name='home'),
    path('list/', views.GameListView.as_view(), name='list'),
    path('form/', views.form, name='form'),
    path('analytics/', views.analytics, name='analytics'),
    path('confirm_delete/', views.confirm_delete, name='confirm_delete'),
    path('games/<int:pk>/', views.GameDetailView.as_view(), name='game_detail'),
]
