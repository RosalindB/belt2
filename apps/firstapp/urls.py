from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'register$', views.submit_register),
    url(r'quotes$', views.logon),
    url(r'^submit_quote$', views.submit_quote),
    url(r'^users/(?P<id>[0-9]+)$', views.uprof),
    url(r'^signin$', views.submit_signin),
    url(r'^logout$', views.logout),
    url(r'^quote/add/(?P<id>[0-9]+)$', views.add_quote),
    url(r'^quote/remove/(?P<id>[0-9]+)$', views.remove_quote),
]