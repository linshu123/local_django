import cgi
import urllib
import simplejson

FACEBOOK_APP_ID = '359702040796778'
FACEBOOK_API_SECRET = 'f5d49fae3d32286be4406d0e04f944f2'
FACEBOOK_REDIRECT_URI = 'http://localhost:8080/login_facebook'

access_token = 'CAAFHJahd3moBAIrnn90fTWYG6aisXF9f5D0CaJGpqz4CZBkr4XGT2XlbsvQExoMAwRyhzZBEGCbOG89ee4Kdreys6HS8PaemGhl0rwhxQ5d9gkt6pgFQdFD9Ct2b4VhGFZAuR5OZAZAZCDsst9nZCa8ta220ywypu4ZD'

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

def get_access_token():
    args = {
                'client_id': FACEBOOK_APP_ID,
                'redirect_uri': FACEBOOK_REDIRECT_URI,
                'client_secret': FACEBOOK_API_SECRET,
                'code': request.GET['code'],
            }
    url = 'https://graph.facebook.com/oauth/access_token?' + \
                    urllib.urlencode(args)
    response = cgi.parse_qs(urllib.urlopen(url).read())
    access_token = response['access_token'][0]
    return access_token;

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
