var games = angular.module('gamesApp', []);

games.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('{[{');
  $interpolateProvider.endSymbol('}]}');
});

function gamesController($scope, $http, $timeout) {
    // get a list of completed games
    var getAvailableGames = function(){
        $http.get($(".available_games").attr("data-url"))
        .success(function(data) {
            $scope.availableGames = data.games;
        })
        .error(function(data) {
            displayMessage(".available_games", data);
        });
    }

    var getConcludedGames = function(){
        // get a list of concluded games
        $http.get($(".concluded_games").attr("data-url"))
        .success(function(data) {
            $scope.concludedGames = data.games;
        })
        .error(function(data) {
            displayMessage(".concluded_games", data);
        });
    }

    // get a list of games the user is currently playing.
    var getCurrentlyPlaying = function(){
        $http.get($(".currently_playing").attr("data-url"))
        .success(function(data) {
            $scope.currentlyPlaying = data.games;

        })
        .error(function(data) {
            displayMessage(".currently_playing", data);
        });
    }

    var poller = function() {
         getAvailableGames();
         getCurrentlyPlaying();
         getConcludedGames();
         $timeout(poller, 20000);
    };

    poller();
}


function displayMessage(parent, message){
    $(parent + " .message").html(message).css("display","block");
}
