from django.conf.urls import patterns, include, url

from django.contrib import admin
from mysite import views

admin.autodiscover()

urlpatterns = patterns('',
	# url(r'^$', 'mysite.views.home', name='home'),

    # for Max's facebook login
    # url(r'^main/index.html', 'fb_login_test.views.login', name='login'),

    # url(r'^login_facebook/?', 'fb_login_test.views.login', name='login_facebook'),
    # url(r'^logged_in_facebook/?', 'fb_login_test.views.show_login_view', name = 'logged_in_facebook'),

    # url(r'^logout.html', 'fb_login_test.views.logout', name='logout'),
    # url(r'^logout/?', 'fb_login_test.views.logout', name='logout'),



    # url(r'^get_friends_name_uid/?', 'fb_login_test.views.get_friends_name_uid', name='get_friends_name_uid'),


    # For social_auth
    # url(r'', include('social_auth.urls')),
    # url(r'^login/$', redirect_to, {'url':'/login/facebook'}),

	url(r'^$', views.all_sites, name='all_sites'),
    url(r'^polls/', include('polls.urls', namespace="polls")),
    url(r'^fb_login_test/', include('fb_login_test.urls', namespace="fb_login_test")),
    url(r'^auth_test/', include('auth_test.urls', namespace="auth_test")),
    url(r'^pull_movies_test/', include('pull_movies_test.urls', namespace="pull_movies_test")),
    # url(r'^facebook_app/', include('facebook_app.urls', namespace="facebook_app")),
    url(r'^admin/', include(admin.site.urls)),
)