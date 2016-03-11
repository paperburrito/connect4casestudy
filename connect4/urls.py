from django.conf.urls import url
import views

urlpatterns = [
    url(r'^games/$', views.games),
    url(r'^play/$', views.play),
]
