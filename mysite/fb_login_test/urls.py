from django.conf.urls import patterns, url
from fb_login_test import views

urlpatterns = patterns('',

    url(r'^$', views.login, name='login'),

    )