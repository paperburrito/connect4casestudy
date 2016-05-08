from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from .models import *

def is_logged_in(function):
  def wrap(request, *args, **kwargs):
    # This checks if a user has registered a business
    if request.user.is_authenticated():
        # If the user is already logged in, redirect to the games page, otherwise they  get a login page
        return HttpResponseRedirect(reverse("games"))
    return function(request, *args, **kwargs)

  wrap.__doc__=function.__doc__
  wrap.__name__=function.__name__
  return wrap
