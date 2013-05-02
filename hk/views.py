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
                'new_list' : Item.objects.filter(type = 'NEW').order_by('-score')
            })

def user(request):
    u = get_object_or_404(Hacker, id = request.GET['id'])
    return render(request, 'user.html', 
            { 
                'page_list' : PAGE_LIST,
                'u' : u 
            })

def submissions(request):
    pass

def comments(request):
    pass

def newcomments(request):
    return render(request, 'index.html', 
            {
                'page_list' : PAGE_LIST,
                'new_list' : Item.objects.filter(type = 'COMMENT').order_by('create_date')
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
    try:
        item = Item.objects.get(id = request.GET['id'])
        item.points_inc()
        item.save()
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
def changepw(request):
    return render(request, 'changepw.html')

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
        return HttpResponseRedirect('/user?id=%d' % u.id)

    except Exception, e:
        return HttpResponse(e)

def hk_logout(request):
    logout(request)
    return HttpResponseRedirect('/')
