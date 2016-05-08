import json

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import Http404, HttpResponseRedirect
from django.utils.translation import ugettext as _

# Django Rest Framework
from rest_framework import status
from rest_framework.decorators import api_view,  permission_classes
from rest_framework.response import Response

# Local Django modules
from .forms import *
from .models import *
from .serializers import *
from .permissions import PlayGamesPermission

GRID_PROPORTIONS = {"columns":7, "rows":6}

@api_view(['GET'])
@permission_classes((PlayGamesPermission,))
def new_game(request):
    game = Game(player1=request.user)
    try:
        game.save()
    except:
         return Response("Failed to create a game", status=status.HTTP_400_BAD_REQUEST)
    return HttpResponseRedirect(reverse("play", kwargs={"game_id":game.id}))

@api_view(['GET'])
@permission_classes((PlayGamesPermission,))
def join_game(request, game_id):
    try:
        game = Game.objects.get(id=game_id)
    except Game.DoesNotExist:
        return Response("This games doesn't exist", status=status.HTTP_404_NOT_FOUND)

    if game.player2:
        return Response("The game has already started", status=status.HTTP_400_BAD_REQUEST)
    game.join_up(request.user)
    return HttpResponseRedirect(reverse("play", kwargs={"game_id":game.id}))


@api_view(['GET'])
@permission_classes((PlayGamesPermission,))
def game_session(request, game_id):
    try:
        game = Game.objects.get(id=game_id)
    except Game.DoesNotExist:
        return Response("This games doesn't exist", status=status.HTTP_404_NOT_FOUND)

    # Now that we know the game exists lets look for any coins that have been registered already.
    coins = Coin.objects.filter(game=game)
    game_instance = game_grid(request, game, coins)

    # I need to figure out if the person has won as well. -- I ran out of time before being able to do this section.
    winner = None
    # success = check_grid(game_instance)
    # if success:
    #     winner = success

    # if no coins have been entered then it's player1's turn
    if len(coins) == 0 and game.player1 == request.user:
        player = player = "Your"
    else:
        # else get the last player to entger a token
        player =  coins.latest("created_date").player

    serializer = GameSessionSerializer(game, context={"game_instance": game_instance, "player_turn":str(player), "winner": str(winner)})
    return Response({"game":serializer.data})

def create_grid():
    # This function creates a blank connect4 grid
    grid = []
    r = 0
    c = 0
    while r < GRID_PROPORTIONS["rows"]:
        row = []
        while c < GRID_PROPORTIONS["columns"]:
            row.append(None)
            c = c + 1
        grid.append(row)
        c = 0
        r = r + 1
    return grid

def populate_grid(grid, game, coins):
    # This function creates a blank connect4 grid
    if len(coins) == 0:
        return grid

    for coin in coins:
        player = "player1"
        if coin.player != game.player1:
            player = "player2"
        grid[coin.row][coin.column -1] = player
    grid.reverse()
    return grid

def game_grid(request, game, coins):
    # this function creates a game grid and populates it with any coins that have been added.
    grid = create_grid()

    # Next time to populate it with any coins.
    grid = populate_grid(grid, game, coins)
    return grid

@api_view(['GET'])
@permission_classes((PlayGamesPermission,))
def add_coin(request, game_id, column):
    column = int(column)
    try:
        game = Game.objects.get(id=game_id)
    except Game.DoesNotExist:
        return Response("This games doesn't exist", status=status.HTTP_404_NOT_FOUND)

    if game.player1 != request.user and game.player2 != request.user:
        return Response("You are not a participant of this game.", status=status.HTTP_401_UNAUTHORIZE)

    # get all coins associated with the game
    coins = Coin.objects.filter(game=game)

    # is this a fresh instance with no coins placed and is the user player1?
    if len(coins) == 0 and game.player1 != request.user:
        return Response("Please wait for {0} to take their turn".format(game.player1), status=status.HTTP_400_BAD_REQUEST)
    elif len(coins) > 0:
        # who was last to add a coin
        last_move = coins.latest("created_date")
        if last_move.player == request.user:
            player = game.player1
            if game.player1 == request.user:
                player = game.player2
            return Response("Please wait for {0} to take their turn".format(player), status=status.HTTP_400_BAD_REQUEST)

    coin_total_in_column = coins.filter(column=column).count()

    # if the coin is out of bounds of the grid
    if column not in range(1, GRID_PROPORTIONS["columns"] + 1) or coin_total_in_column  not in range(0, GRID_PROPORTIONS["rows"]):
        return Response("Can't add a coin here", status=status.HTTP_400_BAD_REQUEST)

    # lets now add a coin
    game.make_move(request.user, coin_total_in_column, column)
    return Response("Coin added")



