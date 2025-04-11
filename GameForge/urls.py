from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('game/<int:game_id>/', views.game_detail, name='game_detail'),
    path('game/generate/', views.generate_view, name='generate_game'),
] 