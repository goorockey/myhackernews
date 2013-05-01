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
        if 'parent' in request.POST:
            parent = Item.objects.get(id = request.POST['parent'])
            
            if 'text' not in request.POST:
                return HttpResponseRedirect('/')
            text = request.POST['text']

            item = Item(type = 'COMMENT', text = text, parent = parent, author = Hacker.objects.get(id = request.user.id))
            item.save()

            parent.set_comments(parent.comments + 1)
            parent.save()

        else:
            if 'title' not in request.POST:
                return HttpResponseRedirect('/')

            title = request.POST['title']
            url = request.POST['url'] if 'url' in request.POST else ''
            text = request.POST['text'] if 'text' in request.POST else ''

            if not (url or text):
                return HttpResponseRedirect('/')

            item = Item(type = 'NEW', title = title, url = url, text = text, author = Hacker.objects.get(id = request.user.id))

            item.save()

        return HttpResponseRedirect('/item?id=%d' % item.id)

    except Exception, e:
        return HttpResponse(e)


def user(request):
    pass

def hk_logout(request):
    logout(request)
    return HttpResponseRedirect('/')
