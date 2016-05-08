var games = angular.module('connect4App', []);

games.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('{[{');
  $interpolateProvider.endSymbol('}]}');
});

games.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

function connect4Controller($scope, $http, $timeout) {
    // get a list of completed games
    var getGameSession = function(){
        $http.get($("#game").attr("data-game-session-url"))
        .success(function(data) {
            $scope.gameSession = data.game;
        })
        .error(function(data) {
            displayMessage(data);
        });
    }


    $scope.addCoin  =  function(column){
        var url = $("#game").attr("data-add-coin-url").split('/');
        url.pop();
        url.push(column);
        url = url.join("/");
        $http.get(url)
        .success(function(data) {
            getGameSession();
        })
        .error(function(data) {
            displayMessage(data);
        });
    }

    var poller = function() {
         getGameSession();
         $timeout(poller, 2000);
    };

    poller();

}

function displayMessage(message){
    $("#message").html(message).slideDown("fast");
    setTimeout(function(){ $("#message").slideUp("fast")}, 5000);
}


