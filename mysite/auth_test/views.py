from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, models, login, logout
from django.db import IntegrityError
from fb_login_test import views as fb_login_test_views

def index(request):
    if request.user.is_authenticated():
        return authenticated(request)
    else:
        return render(request, 'auth_test/index.html', {'message': ''})

def login_user(request):
    if request.user.is_authenticated():
        return authenticated(request)
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username = username, password = password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return authenticated(request)
        else:
            return failed_auth(request)
    else:
        return invalid_login(request)


def create_account(request):
    username = request.POST['username']
    password = request.POST['password']
    password_copy = request.POST['password_copy']
    if (password_copy != password):
        return render(request, 'auth_test/index.html', {'message': 'Password does not match.'})

    # Create a new user and render logged in page
    try:
        user = models.User.objects.create_user(username = username, password = password)
        user.save()
        user = authenticate(username = username, password = password)
        login(request, user)
    except IntegrityError:
        return render(request, 'auth_test/index.html', {'message': 'Username already taken.'})
    
    return authenticated(request)

def logout_user(request):
    logout(request)
    return index(request)

def failed_auth(request):
    return render(render, 'auth_test/failed_auth.html')

def invalid_login(request):
    return render(render, 'auth_test/invalid_login.html')

def authenticated(request):
    return fb_login_test_views.logging_in(request)

def not_authenticated(request):
    return render(request, 'auth_test/not_authenticated.html')