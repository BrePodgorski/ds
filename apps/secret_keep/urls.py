from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^secrets$', views.secrets),
    url(r'^login$', views.login),
    url(r'^post_secret$', views.post_secret),
    url(r'^logout_view$', views.logout_view),
    url(r'^secrets/(?P<my_secret_id>\d+)/likes$', views.add_like),
    url(r'^secrets/(?P<my_secret_id>\d+)/destroy$', views.destroy)
]
