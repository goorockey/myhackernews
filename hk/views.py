from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import render, get_object_or_404
from hk.models import *

PAGE_LIST = {'new' : '/newest', 'comments' : '/comments', 'submit': '/submit'}
PAGE_ITEM_COUNT = 60
ITEM_UPLIMIT = 1500

def index(request):
    try:
        item_list = Item.objects.filter(type = 'NEW').order_by('-score')
        if 'id' in request.GET:
            item_list = item_list.filter(author_id = request.GET['id'])

        start = int(request.GET['s']) if 's' in request.GET else 0

        next = start + PAGE_ITEM_COUNT
        if next >= item_list.count() or next >= ITEM_UPLIMIT:
            next = -1

        return render(request, 'index.html', 
                {
                    'page_list' : PAGE_LIST,
                    'item_list' : item_list[start : start + PAGE_ITEM_COUNT],
                    'start' : start,
                    'next' : next
                })
    except Exception, e:
        return HttpResponse(e)

def newest(request):
    try:
        item_list = Item.objects.filter(type = 'NEW').order_by('create_date')
        if 'id' in request.GET:
            item_list = item_list.filter(author_id = request.GET['id'])

        start = int(request.GET['s']) if 's' in request.GET else 0

        next = start + PAGE_ITEM_COUNT
        if next >= item_list.count() or next >= ITEM_UPLIMIT:
            next = -1

        return render(request, 'index.html', 
                {
                    'page_list' : PAGE_LIST,
                    'item_list' : item_list[start : start + PAGE_ITEM_COUNT],
                    'start' : start,
                    'next' : next
                })
    except Exception, e:
        return HttpResponse(e)

def user(request):
    u = get_object_or_404(Hacker, id = request.GET['id'])
    return render(request, 'user.html', 
            { 
                'page_list' : PAGE_LIST,
                'u' : u 
            })

def comments(request):
    try:
        item_list = Item.objects.filter(type = 'COMMENT').order_by('create_date')
        if 'id' in request.GET:
            item_list = item_list.filter(author_id = request.GET['id'])

        start = int(request.GET['s']) if 's' in request.GET else 0
        next = start + PAGE_ITEM_COUNT
        if next >= item_list.count() or next >= ITEM_UPLIMIT:
            next = -1

        return render(request, 'comments.html', 
                {
                    'page_list' : PAGE_LIST,
                    'item_list' : item_list[start : start + PAGE_ITEM_COUNT],
                    'start' : start,
                    'next' : next
                })
    except Exception, e:
        return HttpResponse(e)

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
    try:
        item = Item.objects.get(id = request.GET['id'])
        item.points_inc()
        return HttpResponse('OK')

    except Exception, e:
        return  HttpResponse(e)

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

            parent.comments_inc()

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

@login_required
def update(request):
    try:
        about = request.POST['about']
        email = request.POST['email']
        
        item = Item.get_object_or_404(Item, id = request.user.id)
        item.about = about
        item.email = email
        item.save()
        return HttpResponseRedirect('/user?id=%d' % user.id)

    except Exception, e:
        return HttpResponse(e)

@login_required
def password(request):
    try:
        pw1 = request.POST['new_password1']
        pw2 = request.POST['new_password1']
        if pw1 != pw2:
            return HttpResponse('password error')

        u = get_object_or_404(Hacker, id = request.user.id)
        u.set_password(pw1)
        u.save()
        return HttpResponseRedirect('/pwchanged')

    except Exception, e:
        return HttpResponse(e)

def hk_logout(request):
    logout(request)
    return HttpResponseRedirect('/')
