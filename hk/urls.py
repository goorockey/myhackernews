from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'hk.views.index', name='index'),
    url(r'^comments$', 'hk.views.comments', name='comments'),
    url(r'^item$', 'hk.views.item', name='item'),
    url(r'^submit$', 'hk.views.submit', name='submit'),
    url(r'^reply$', 'hk.views.reply', name='reply'),
    url(r'^vote$', 'hk.views.vote', name='vote'),
    url(r'^r$', 'hk.views.response', name='response'),
    url(r'^login$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout$', 'hk.views.hk_logout', name='logout'),
    url(r'^user$', 'hk.views.user', name='user'),
    # url(r'^hk/', include('hk.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
