from django.contrib import admin
from django.urls import path
from games import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('games/', views.GameListView.as_view(), name='game_list'),
    path('games/<int:pk>/', views.GameDetailView.as_view(), name='game_detail'),
    path('games/add/', views.game_add, name='game_add'),
    path('games/<int:pk>/edit/', views.game_add, name='game_edit'),
    path('games/<int:pk>/delete/', views.confirm_delete, name='confirm_delete'),
    path('analytics/', views.analytics, name='analytics'),
]
