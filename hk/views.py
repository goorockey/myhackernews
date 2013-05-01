from django.http import HttpResponse
from django.shortcuts import render
from hk.models import *

page_list = {'new' : '/', 'comments' : '/comments', 'submit': '/submit'}

def index(request):
    return render(request, 'index.html', 
            {'page_list': page_list,
             'new_list' : New.objects.all()})
