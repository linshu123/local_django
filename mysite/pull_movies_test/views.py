from django.shortcuts import render_to_response
from mysite import settings

def show_main_page(request):
    return display_movies(request)

def display_movies(request):
    return render_to_response('pull_movies_test/main.html', {'FACEBOOK_APP_ID': settings.FACEBOOK_APP_ID})