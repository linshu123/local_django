from django.conf.urls import patterns, url
from django.views.generic import DetailView, ListView

from auth_test import views
urlpatterns = patterns('', 
    url(r'^$', views.index, name = 'index'),
    url(r'^login_user/$', views.login_user, name = 'login_user'),
    url(r'^create_account/$', views.create_account, name = 'create_account'),
    url(r'^logout_user/$', views.logout_user, name = 'logout_user'),
    )