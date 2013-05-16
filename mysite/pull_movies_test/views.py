from django.shortcuts import render_to_response

def show_main_page(request):
    return render_to_response('pull_movies_test/main.html')

def display_movies(request):
    return render_to_response('pull_movies_test/main.html')