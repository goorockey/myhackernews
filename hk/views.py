from django.http import HttpResponse, Http404
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

COMMENTS_TEMPLATE = '''
<tr>
    <td>
        <table>
            <tbody>
                <tr>
                    <td>
                        <div width="%(padding)"></div>
                    </td>
                    <td>
                        <a href="/vote?id=%(item_id)&u=%(user_id)"><img class="vote_img" src="{% static 'img/grayarrow.gif' %}" /></a>
                    </td>
                    <td>
                        <span class="item_info">
                            <a href="/user?id={{ item.author.id }}">{{ item.author.username }}</a>
                            {{ item.formated_create_time }}
                            | 
                            <a href="item?id={{ item.id }}">{{ item.comments }} comments</a>
                            |
                            <a href="item?id={{ item.parent_id }}">parent</a>
                        </span>
                        <span class="content" >%(content)</span>
                        <p><a href="reply?id=%(item_id)&u=%(user_id)">reply</a></p>
                    </td>
                </tr>
            </tbody>
        </table>
    </td>
</tr>
'''

def getComments(item, level = [], comments = []):
    if item.parent:
        comments.append(COMMENTS_TEMPLATE % 
                {
                    'padding' : level[0] * 40,
                    'item_id' : item.id,
                    'content' : item.text,
                    'user_id' : 0,
                })

    level[0] = level[0] + 1
    for item in Item.objects.filter(parent__id = item.id):
        getComments(item, level, comments)

def item(request):
    try:
        item = get_object_or_404(Item, id = request.GET['id'])
        level = [0]
        comments = []
        getComments(item, level, comments)
        return render(request, 'item.html', 
                {
                    'page_list' : PAGE_LIST,
                    'item' : item,
                    'comments' : ''.join(comments),
                })
    except Exception, e:
        #return Http404
        return HttpResponse(e)

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
