# Create your views here.
import cgi
import urllib
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import models as auth_models
from django.core.context_processors import csrf
from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render, redirect
from django.views.decorators.csrf import ensure_csrf_cookie
from mysite import settings
import fb_login_test
from django.core.exceptions import ObjectDoesNotExist
import simplejson


login_view_url = 'fb_login_test/login_view.html'

@ensure_csrf_cookie
def show_login_view(request):
    if request.user.is_authenticated():
        return logging_in(request)
    return render(request, 'auth_test/index.html', {'message': ''})


def logging_in(request):
    show_friends_view_url = 'fb_login_test/logged_in_view.html'
    if 'code' in request.GET:
        args = {
            'client_id': settings.FACEBOOK_APP_ID,
            'client_secret': settings.FACEBOOK_API_SECRET,
            'redirect_uri': settings.FACEBOOK_REDIRECT_URI,
            'code': request.GET['code'],
        }

        url = 'https://graph.facebook.com/oauth/access_token?' + urllib.urlencode(args)
        response = cgi.parse_qs(urllib.urlopen(url).read())
        access_token = response['access_token'][0]
        facebook_session, created = fb_login_test.models.FacebookSession.objects.get_or_create(user = request.user, access_token = access_token)
        if created:
            facebook_session.save()

    elif request.user.is_authenticated():
        try:
            facebook_session = fb_login_test.models.FacebookSession.objects.get(user=request.user)
            
        except ObjectDoesNotExist:
            fb_login_url = 'https://graph.facebook.com/oauth/authorize?client_id=' + settings.FACEBOOK_APP_ID + '&redirect_uri=' + settings.FACEBOOK_REDIRECT_URI + '&scope=user_photos,friends_photos&display=popup'
            return redirect(fb_login_url)

        access_token = facebook_session.access_token

    else:
        return render_to_response('auth_test/not_authenticated.html')

    
    friends_list = get_friends(access_token)

    friends_names = []
    for friend in friends_list:
        element = {
            'full_name': friend['first_name'] + " " + friend['last_name'],
            'id': friend['uid'],
        }
        friends_names.append(element)

    return render(request, show_friends_view_url, {'friends_list':friends_names})


def logout_user(request):
    logout(request)
    return show_login_view(request)

def query_fql_get_data(query, access_token):
    url = 'https://graph.facebook.com/fql?q=' + query + '&access_token=%s' % \
        (access_token)
    response = simplejson.load(urllib.urlopen(url))
    return response['data']

def get_me(access_token):

    query = 'SELECT+uid,+first_name,+last_name+FROM+user+WHERE uid = me()'
    response = query_fql_get_data(query, access_token)
    return response[0]

def get_friends(access_token):

    query = 'SELECT+uid,+first_name,+last_name+FROM+user+WHERE+uid+\
        IN+(SELECT+uid2+FROM+friend+WHERE+uid1=me())'
    return query_fql_get_data(query, access_token)




