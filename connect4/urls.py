from django.conf.urls import url
from .import views, api, game_api

urlpatterns = [
    url(r'^login/$', views.login, name='login'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^games/$', views.games, name='games'),
    url(r'^play/(?P<game_id>\d+)$', views.play, name='play'),


    # API
    url(r'^api/currently_playing/$', api.currently_playing, name='currently_playing'),
    url(r'^api/available_games/$', api.available_games, name='available_games'),
    url(r'^api/concluded_games/$', api.concluded_games, name='concluded_games'),

    # api end points for creating a new game and playing it
    url(r'^api/new_game/$', game_api.new_game, name='new_game'),
    url(r'^api/join_game/(?P<game_id>\d+)$', game_api.join_game, name='join_game'),
    url(r'^api/game/(?P<game_id>\d+)/session/$', game_api.game_session, name='game_session'),
    url(r'^api/game/(?P<game_id>\d+)/add_coin/(?P<column>\d+)$', game_api.add_coin, name='add_coin'),

]
