from django.conf.urls import patterns, url
from fb_login_test import views

urlpatterns = patterns('',

    url(r'^$', views.show_login_view, name='show_login_view'),
    # url(r'^$', views.test_view, name='show_login_view'),
    url(r'^logging_in/?', views.logging_in, name='logging_in'),


    )