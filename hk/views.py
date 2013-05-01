from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from hk.models import *

page_list = {'new' : '/', 'comments' : '/comments', 'submit': '/submit'}

def index(request):
    return render(request, 'index.html', 
            {
                'page_list' : page_list,
                'new_list' : Item.objects.filter(type = 'NEW')
            })

def comments(request):
    return render(request, 'index.html', 
            {
                'page_list' : page_list,
                'new_list' : Item.objects.filter(type = 'COMMENT')
            })

def item(request):
    try:
        item = get_object_or_404(Item, id = request.GET['id'])
        return render(request, 'index.html', 
                {
                    'page_list' : page_list,
                    'item' : item,
                })
    except Exception, e:
        return HttpResponse(e)
        #raise Http404

def submit(request):
    return render(request, 'submit.html')

def vote(request):
    pass

def login(request):
    pass

def logout(request):
    pass

def response(request):
    pass
