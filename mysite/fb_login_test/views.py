# Create your views here.
import cgi
import urllib
from fb_login_test.modules.facebook import facebook_views
from django.core.context_processors import csrf
from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.views.decorators.csrf import ensure_csrf_cookie
from mysite import settings
import simplejson

# for max's facebook login
# def show_login_view(request):
#     return facebook_views.show_login_view(request) 

# def login(request):
#     return facebook_views.login_view(request)

# def logout(request):
#     return facebook_views.logout_view(request)

# def get_friends_name_uid(request):
#     return facebook_views.get_friends_name_uid(request);

# def test_view(request):
#     return(request, '/auth_test/.html', {'message':''})

@ensure_csrf_cookie
def show_login_view(request):
    login_view_url = 'fb_login_test/login_view.html'
    context = {
        'settings.FACEBOOK_REDIRECT_URI': settings.FACEBOOK_REDIRECT_URI,
        'settings.FACEBOOK_APP_ID': settings.FACEBOOK_APP_ID,
    }
    return render(request, login_view_url, context)


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
    expires = response['expires'][0]
    friends_list = get_friends(access_token)
    return render(request, show_friends_view_url, {'friends_list':friends_list})


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




