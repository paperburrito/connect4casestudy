
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404, get_list_or_404
from django.template import loader
from django.views.decorators.http import  require_http_methods
from django.views.decorators.csrf import ensure_csrf_cookie

from .models import  *
from .forms import LoginForm, SignUpForm
from .decorators import is_logged_in

# Create your views here.

@require_http_methods(["GET", "POST"])
@ensure_csrf_cookie
@is_logged_in
def login(request):
    if request.user.is_authenticated():
        # If the user is already logged in, redirect to the games page, otherwise they  get a login page
        return HttpResponseRedirect(reverse("games"))

    form = LoginForm(request.POST or None)
    if request.POST and form.is_valid():
        user = form.login(request)
        if user:
            auth.login(request, user)
            # if the user tried to gain access to another page before logging in, then redirect \
            # them to that page instead of the games page.
            next_url = request.GET.get("next", None)
            if next_url is not None:
                return HttpResponseRedirect(next_url)
            return HttpResponseRedirect(reverse("games"))

    t = loader.get_template("login.html")
    return HttpResponse(t.render({"FORM":form}, request))


@require_http_methods(["GET"])
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse("login"))


@require_http_methods(["GET", "POST"])
@ensure_csrf_cookie
@is_logged_in
def signup(request):
    form = SignUpForm(request.POST or None)
    if request.POST and form.is_valid():
        user = form.create_user()
        user = auth.authenticate(username=form.cleaned_data["username"],
                                 password=form.cleaned_data["password"])
        if user:
            auth.login(request, user)
            return HttpResponseRedirect(reverse("games"))

    t = loader.get_template("signup.html")
    return HttpResponse(t.render({"FORM":form}, request))


@require_http_methods(["GET"])
@ensure_csrf_cookie
@login_required
def games(request):
    """
    Write your view which controls the game set up and selection screen here
    :param request:
    :return:
    """
    t = loader.get_template("games.html")
    return HttpResponse(t.render({}, request))


@require_http_methods(["GET"])
@login_required
def play(request, game_id):
    """
    write your view which controls the gameplay interaction w the web layer here
    :param request:
    :return:
    """
    try:
        game = Game.objects.get(id=game_id)
    except Game.DoesNotExist:
        return HttpResponse("Game doesn't exist")

    if game.player1 != request.user and  game.player2 != request.user:
        if game.player2 == None:
            game.join_up(request.user)

    if game.player1 == request.user or  game.player2 == request.user:
        t = loader.get_template("play.html")
        return HttpResponse(t.render({"GAME":game}, request))


