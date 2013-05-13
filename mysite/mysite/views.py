from polls.models import Choice, Poll
from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponse
from django.template import Context, loader

def all_sites(request):
	return render(request, 'home/index.html', ) 


# def all_sites(request):
#     return render(request, 'home/javascript_site.html') 
