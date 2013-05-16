from django.conf.urls import patterns, url

from pull_movies_test import views

urlpatterns = patterns('', 

    url(r'^$', views.show_main_page, name = 'show_main_page'),
    url(r'^display_movies/$', views.display_movies, name = 'display_movies'),

    )
