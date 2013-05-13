# Create your views here.

from fb_login_test.modules.facebook import facebook_views

from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.decorators.csrf import ensure_csrf_cookie


# for max's facebook login
@ensure_csrf_cookie
def show_login_view(request):
    return facebook_views.show_login_view(request) 

def login(request):
    return facebook_views.login_view(request)

def logout(request):
    return facebook_views.logout_view(request)

def get_friends_name_uid(request):
    return facebook_views.get_friends_name_uid(request);
