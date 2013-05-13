# facebook.py defines views for facebook login / logout
import cgi
import urllib

from django.contrib import auth
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.context_processors import csrf
from fb_login_test import models
import simplejson

# from facebook_app.views import authed_index_with_token

from mysite import settings
from fb_login_test import models

# If logged in or authenticated, use this function to display the friends list.
def show_login_view(request):
    logged_in_redirect_url = '/fb_login_test/fb_login_test_index.html'
    # try:
    #     facebook_session = models.FacebookSession.objects.get(user=request.user)
    # except FacebookSession.DoesNotExist:
    #     return
    facebook_session = models.FacebookSession.objects.get(user=request.user)
    access_token = facebook_session.access_token
    friends_list = get_friends(access_token)
    friends_names = [friend_name['first_name'] + ' ' + friend_name['last_name'] for friend_name in friends_list]
    context = {
        'friends_list':friends_names
    }
    return render_to_response(logged_in_redirect_url, context, 
    context_instance = RequestContext(request))

def login_view(request):
    error = None
    not_logged_in_url = 'fb_login_test/not_logged_in.html'

    # if request.user.is_authenticated():
    #     return show_login_view(request)
        # return HttpResponseRedirect(logged_in_redirect_url)
        # return authed_index_with_token(request, access_token)

    if request.GET:
        if 'code' in request.GET:
            args = {
                'client_id': settings.FACEBOOK_APP_ID,
                'redirect_uri': settings.FACEBOOK_REDIRECT_URI,
                'client_secret': settings.FACEBOOK_API_SECRET,
                'code': request.GET['code'],
            }

            url = 'https://graph.facebook.com/oauth/access_token?' + \
                    urllib.urlencode(args)
            response = cgi.parse_qs(urllib.urlopen(url).read())
            access_token = response['access_token'][0]
            expires = response['expires'][0]

            facebook_session = models.FacebookSession.objects.get_or_create(
                access_token=access_token,
            )[0]

            facebook_session.expires = expires
            facebook_session.save()

            user = auth.authenticate(token=access_token)
            if user:
                if user.is_active:
                    auth.login(request, user)
                    return show_login_view(request)
                    # return HttpResponseRedirect(logged_in_redirect_url)
                    # return authed_index_with_token(request, token=access_token)
                else:
                    error = 'AUTH_DISABLED'
            else:
                error = 'AUTH_FAILED'
        elif 'error_reason' in request.GET:
            error = 'AUTH_DENIED'

    # Generates the csrf token
    c = {}
    c.update(csrf(request))
    template_context = dict({'settings': settings, 'error': error}.items() +\
                            c.items())
    return render_to_response(not_logged_in_url, template_context,
            context_instance=RequestContext(request))

def logout_view(request):
    auth.logout(request)
    return HttpResponseRedirect(not_logged_in_url)


# sends fql query to facebook
# returns data in the response
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


# query all friends, plus me
def get_users(access_token):

    query = 'SELECT+uid,+first_name,+last_name+FROM+user+WHERE+uid+\
        IN+(SELECT+uid2+FROM+friend+WHERE+uid1=me()) OR uid = me()'
    return query_fql_get_data(query, access_token)


# queries facebook with FQL to get names and uids of all friends of current user
def get_friends_name_uid_fql(request):
    facebook_session = models.FacebookSession.objects.get(user=request.user)

    friends_list = get_friends(facebook_session.access_token)

    friends_name_uid_list = []
    for friend in friends_list:
        element = {
            'label': friend['first_name'] + " " + friend['last_name'],
            'value': friend['uid'],
        }
        friends_name_uid_list.append(element)
    return friends_name_uid_list


# ajax call for returning json objects
def get_friends_name_uid(request):

    friends_name_uid_list = get_friends_name_uid_fql(request)
    return HttpResponse(simplejson.dumps(friends_name_uid_list), \
        content_type="text/json")

