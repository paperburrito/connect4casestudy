# Local Django modules
from .models import Game

# Django
from django.conf import settings
from django.core.urlresolvers import reverse

# Django Rest Framework
from rest_framework import serializers


class GamesListSerializer(serializers.ModelSerializer):
    # Note: The UI just displays whatever the format is here.
    player1 = serializers.SerializerMethodField()
    player2 =  serializers.SerializerMethodField()
    link = serializers.SerializerMethodField()

    def get_player1(self, game):
        return game.player1.username

    def get_player2(self, game):
        if game.player2 is None:
            return "Waiting for opponent"
        return game.player2.username

    def get_link(self, game):
        return reverse("play", kwargs={"game_id":game.id})

    class Meta:
        model = Game
        fields = ("player1",
                      "player2",
                      "link")


class GameSessionSerializer(serializers.ModelSerializer):
    player1 = serializers.SerializerMethodField()
    player2 =  serializers.SerializerMethodField()
    player_turn =  serializers.SerializerMethodField()
    winner =  serializers.SerializerMethodField()
    game_instance =  serializers.SerializerMethodField()

    def get_player1(self, game):
        return game.player1.username

    def get_player2(self, game):
        if game.player2 is None:
            return "Waiting for opponent"
        return game.player2.username

    def get_player_turn(self, game):
        return self.context["player_turn"]

    def get_winner(self, game):
        return self.context["winner"]

    def get_game_instance(self, game):
        return self.context["game_instance"]

    class Meta:
        model = Game
        fields = ("player1",
                      "player2",
                      "player_turn",
                      "winner",
                      "game_instance")

