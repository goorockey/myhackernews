from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import render, get_object_or_404
from hk.models import *

PAGE_LIST = {'new' : '/', 'comments' : '/comments', 'submit': '/submit'}

def index(request):
    return render(request, 'index.html', 
            {
                'page_list' : PAGE_LIST,
                'new_list' : Item.objects.filter(type = 'NEW')
            })

def comments(request):
    return render(request, 'index.html', 
            {
                'page_list' : PAGE_LIST,
                'new_list' : Item.objects.filter(type = 'COMMENT')
            })

def item(request):
    #try:
    item = get_object_or_404(Item, id = request.GET['id'])
    return render(request, 'item.html', 
            {
                'page_list' : PAGE_LIST,
                'item' : item,
            })
    #except Exception, e:
        #return Http404
        #return HttpResponse(e)

@login_required
def submit(request):
    return render(request, 'submit.html')

@login_required
def vote(request):
    pass

@login_required
def reply(request):
    pass


@login_required
def response(request):
    try:
        parent_id = request.POST['parent']
        text = request.POST['text']

        if parent_id:
            parent = Item.objects.get(id = parent_id)
            item = Item(type = 'COMMENT', text = text, parent = parent, author = Hakcer.objects.get(id = 1))
            item.save()

            parent.set_comments(parent.comments + 1)
            parent.save()

        else:
            title = request.POST['title']
            url = request.POST['url']

            item = Item(type = 'NEW', title = title, url = url, text = text, author = Hacker.objects.get(id = 1))

            item.save()

        return HttpResponseRedirect('/item?id=' + item.id)

    except Exception, e:
        return HttpResponse(e)


def user(request):
    pass

def hk_logout(request):
    logout(request)
    return HttpResponseRedirect('/')
