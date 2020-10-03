from django.urls import include, path, re_path

from . import views

app_name = 'game'
urlpatterns = [
    path('', views.home, name='home'),
    path('index/', views.index, name='index'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('newgame/', views.createNewGame, name='newgame'),
    path('join/<str:urlKey>/', views.joinGame, name='join'),
    path('events/<int:gameId>/', views.getGameEvents, name='events'),
    path('update/<int:gameId>/', views.updatePlayerState, name='update'),
    path('start/<int:gameId>/', views.startGame, name='start'),
]
