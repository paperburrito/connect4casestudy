import json

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import Http404, HttpResponseRedirect
from django.utils.translation import ugettext as _

# Django Rest Framework
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Local Django modules
from .forms import *
from .models import *
from .serializers import *

@api_view(['GET'])
def currently_playing(request):
    games = Game.objects.filter(Q(player1=request.user) | Q(player2=request.user))
    if len(games) == 0:
        return Response("You are currently not playing any games.", status=status.HTTP_404_NOT_FOUND)

    serializer = GamesListSerializer(games,
                                                 context={"request": request},
                                                 many=True)
    return Response({"games":serializer.data})

@api_view(['GET'])
def available_games(request):
    games = Game.objects.exclude(Q(player1=request.user) | Q(player2=request.user))
    if len(games) == 0:
        return Response("There are no available games", status=status.HTTP_404_NOT_FOUND)

    serializer = GamesListSerializer(games,
                                                 context={"request": request},
                                                 many=True)
    return Response({"games":serializer.data})

@api_view(['GET'])
def concluded_games(request):
    games = Game.objects.filter(Q(player1=request.user) | Q(player2=request.user)).exclude(status=IN_PROGRESS)
    if len(games) == 0:
        return Response("You haven't played any games, what's wrong with you? GO PLAY!!", status=status.HTTP_404_NOT_FOUND)

    serializer = GamesListSerializer(games,
                                                         context={"request": request},
                                                         many=True)

    return Response({"games":serializer.data})
